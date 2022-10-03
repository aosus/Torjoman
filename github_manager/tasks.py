import itertools
import json
import os
import re
from pathlib import Path

from django.conf import settings
from django.db.models import Count
from github import Github

from translation.models import SourceTranslation, UserTranslation, Word

from .models import Moderator, PullRequest

account = Github(os.environ.get("GITHUB_ACCOUNT_TOKEN"))
account_id = account.get_user().id
dictionary_repo = account.get_repo(os.environ.get("JSON_REPO"))
local_json_file: Path = (settings.BASE_DIR / "local_dictionary.json").resolve()

if not local_json_file.exists():
    raise Exception(
        "Please run 'python3 project/prepare-project.py' before run Torjoman for the first time"
    )


def check_for_update_json():
    file = dictionary_repo.get_contents(os.environ.get("JSON_FILE"))
    server = json.loads(file.decoded_content)
    local = json.loads(local_json_file.read_text())
    if server == local:
        print("There is no change")
        return
    else:
        print("Files Are not the same")
        update_source(local, server)
        with open(str(local_json_file), "w") as f:
            json.dump(server, f, ensure_ascii=False, indent=2)


def generate_dict_from_db(word: Word) -> list[dict]:
    return [
        {
            "word": w.word,
            "translations": w.get_users_translations
            if w.word == word.word
            else w.get_source_translations,
            "is_checked": w.is_checked,
        }
        for w in Word.objects.all()
    ]


def update_source(local: list[dict], server: list[dict]):
    rlocal = list(itertools.filterfalse(lambda x: x in local, server))
    rserver = list(itertools.filterfalse(lambda x: x in server, local))
    deleted_words: list[str] = [
        x["word"] for x in rserver if x["word"] not in [i["word"] for i in rlocal]
    ]
    for word in deleted_words:
        w: Word = Word.objects.get(word=word)
        w.delete()
    for word in rlocal:
        w: Word = Word.objects.get_or_create(word=word["word"])[0]
        if word["translations"]:
            for translation in word["translations"]:
                st: SourceTranslation = SourceTranslation.objects.get_or_create(
                    word=w, translation=translation
                )[0]
                st.save()
                # Reset users translations
                for translation in w.usertranslation_set.all():
                    translation.delete()
        deleted_translations = [
            SourceTranslation.objects.get(word=w, translation=t)
            for t in w.get_source_translations
            if t not in word["translations"]
        ]
        for translation in deleted_translations:
            translation.delete()


def handle_push(_payload: dict):
    print("New Push Event")
    check_for_update_json()
    print("Finished Push Event")


def handle_pull_request(payload: dict):
    # Verify whether the request is a pull request and if its owner is our account
    if issue := payload.get("issue"):
        if not issue.get("pull_request"):
            pass
    elif pr := payload.get("pull_request"):
        if pr["user"]["id"] != account_id:
            return
    match payload["action"]:
        case "closed":
            PullRequest.objects.get(number=payload["number"]).delete()
            word: str = re.search(r"'(?P<word>.+)'\s", payload["issue"]["title"]).group(
                "word"
            )
            [
                ref
                for ref in dictionary_repo.get_git_refs()
                if ref.ref == f"refs/heads/Torjoman-{word.word}"
            ][0].delete()


def handle_pr_comments(payload):
    number = payload["issue"]["number"]
    if not payload["comment"]["user"]["login"] in Moderator.get_all_moderators():
        return
    r = re.search(
        r"^/(?P<command>.+) (?P<translation>\d+)$", payload["comment"]["body"]
    )
    word: str = re.search(r"^'(?P<word>.+)'\s", payload["issue"]["body"]).group("word")
    translations: dict[str, str] = {
        i: t
        for i, t in re.findall(
            r"(?P<index>\d+)\. '(?P<translation>.+?)'", payload["issue"]["body"]
        )
    }
    print(word, translations)
    match r.group("command"):
        case "set-default":
            w: Word = Word.objects.get(word=word)
            tr: UserTranslation = UserTranslation.objects.get(
                word=w, translation=translations[r.group("translation")]
            )
            tr.score = w.usertranslation_set.first().score + 1
            tr.save()
            update_pull_request(number, w)
        case _:
            pass


def update_json_file(word: Word, translations: list[str]) -> str:
    """update_json_file Update word translations and return json as string.

    Args:
        word (Word): The word to update.
        translations (list[str]): List of translations. Order is important.

    Returns:
        str: updated json file content as string
    """


def update_pull_request(number, word):
    with open(settings.BASE_DIR / "github_manager" / "messages.json") as f:
        messages = json.load(f)["pull_request"]
    pull = dictionary_repo.get_pull(number)
    f = dictionary_repo.get_contents(
        os.environ.get("JSON_FILE"), ref=f"Torjoman-{word.word}"
    )
    dictionary_repo.update_file(
        os.environ.get("JSON_FILE"),
        f"Update {word.word} Translation To {word.usertranslation_set.first()}",
        json.dumps(generate_dict_from_db(word), indent=4, ensure_ascii=False),
        f.sha,
        branch=f"Torjoman-{word.word}",
    )
    body = messages["head"].format(
        word=word.word, translation=word.get_users_translations[0]
    )
    for index, translation in enumerate(word.get_users_translations[:5]):
        body += (
            messages["other_translation"].format(
                index=index + 1, translation=translation
            )
            + "\n"
        )
    body += "\n" + messages["footer"]
    pull.edit(
        title=messages["title"].format(
            word=word.word, translation=word.get_users_translations[0]
        ),
        body=body,
    )


def make_pull_request():
    """make_pull_request Get Words that have at least 5 translations and make a pull request"""
    words: list[Word] = Word.objects.annotate(
        num_usertranslation=Count("usertranslation")
    ).filter(num_usertranslation__gt=3, pullrequest=None)
    if not words:
        return
    with open(settings.BASE_DIR / "github_manager" / "messages.json") as f:
        messages = json.load(f)["pull_request"]
    source_branch = dictionary_repo.get_branch(dictionary_repo.default_branch)
    for word in words:
        try:
            [
                ref
                for ref in dictionary_repo.get_git_refs()
                if ref.ref == f"refs/heads/Torjoman-{word.word}"
            ][0].delete()
        except:
            pass
        dictionary_repo.create_git_ref(
            f"refs/heads/Torjoman-{word.word}", source_branch.commit.sha
        )
        f = dictionary_repo.get_contents(
            os.environ.get("JSON_FILE"), ref=f"Torjoman-{word.word}"
        )
        dictionary_repo.update_file(
            os.environ.get("JSON_FILE"),
            f"Update {word.word} Translation To {word.usertranslation_set.first()}",
            json.dumps(generate_dict_from_db(word), indent=4, ensure_ascii=False),
            f.sha,
            branch=f"Torjoman-{word.word}",
        )
        body = messages["head"].format(
            word=word.word, translation=word.get_users_translations[0]
        )
        for index, translation in enumerate(word.get_users_translations[:5]):
            body += (
                messages["other_translation"].format(
                    index=index + 1, translation=translation
                )
                + "\n"
            )
        body += "\n" + messages["footer"]
        pull = dictionary_repo.create_pull(
            title=messages["title"].format(
                word=word.word, translation=word.get_users_translations[0]
            ),
            body=body,
            head=f"Torjoman-{word.word}",
            base="main",
        )
        PullRequest.objects.create(number=pull.number, word=word)
