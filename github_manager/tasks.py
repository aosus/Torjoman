from .models import PullRequest
from github import Github
import json
import os
from pathlib import Path
from django.conf import settings
import itertools
from translation.models import Word, SourceTranslation

account = Github(os.environ.get("GITHUB_ACCOUNT_TOKEN"))
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


def generate_dict_from_db() -> list[dict]:
    return [
        {
            "word": w.word,
            "translations": w.get_source_translations,
            "is_checked": w.is_checked,
        }
        for w in Word.objects.all()
    ]


def update_source(local: list[dict], server: list[dict]):
    rlocal = list(itertools.filterfalse(lambda x: x in local, server))
    rserver = list(itertools.filterfalse(lambda x: x in server, local))
    deleted_words: str = [
        x["word"] for x in rserver if x["word"] not in [i["word"] for i in rlocal]
    ]
    for word in deleted_words:
        w: Word = Word.objects.get(word["word"])
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


def push(_payload: dict):
    print("New Push Event")
    check_for_update_json()
    print("Finished Push Event")
