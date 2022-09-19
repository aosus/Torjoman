# from translate.models import Word as TWord, Translate as TTranslate
from .models import PullRequest
from github import Github
import json
import os
from pathlib import Path
from django.conf import settings
# from cache_json.models import Word, Translate


account = Github(os.environ.get("GITHUB_ACCOUNT_TOKEN"))
dictionary_repo = account.get_repo(os.environ.get('JSON_REPO'))
local_json_file: Path = (settings.BASE_DIR / 'local_dictionary.json').resolve()

if not local_json_file.exists():
  raise Exception("Please run 'python3 project/prepare-project.py' before run Torjoman for the first time")

def check_for_update_json():
  file = dictionary_repo.get_contents(os.environ.get('JSON_FILE'))
  repo_file_json= json.loads(file.decoded_content)
  old_file_json = json.loads(local_json_file.read_text())
  if repo_file_json == old_file_json:
    return
  else:
    print('Files Are not the same')
    with open(str(local_json_file), 'w') as f:
      json.dump(repo_file_json, f, ensure_ascii=False, indent=2)
    update_source(repo_file_json)

def update_source(data: list[dict[str, str | list]]):
  source_words = [] # store words to check if some words have been deleted
  data_words = []
  
  for word in data:
    data_words.append(word['word'].strip())
    if word['is_checked']:
      print('Skip word {} because it is checked'.format(word['name']))
      w = TWord.objects.get(word=word['word'])
      w.delete()
      continue
    w: Word = Word.objects.get_or_create(word=word['word'])[0]
    w.save()
    for translate in word['translates']:
      try:
        Translate.objects.get(word=w, translate=translate)
      except Translate.DoesNotExist:
        print(f'new translation for word {w.word}')
        t: Translate = Translate.objects.get_or_create(word=w, translate=translate)[0]
        t.save()

        tw: TWord = TWord.objects.get_or_create(word=w.word)[0]
        [t.delete() for t in tw.translate_set.all()]
        [t.delete() for t in tw.prs.all()]
        tt: TTranslate = TTranslate(word=tw, translate=translate)
        tt.save()
  source_words = [w.word for w in Word.objects.all()] 
  diff = list(set(data_words) - set(source_words))
  for word in diff:
    w = Word.objects.get(word=word)
    w.delete()
    w = TWord.objects.get(word=word)
    w.delete()

def push(_payload: dict):
  print('New Push Event')
  check_for_update_json()
  print('Finished Push Event')
  
  
if local_json_file.read_text() == '{}':
  # check_for_update_json()
  print('The first data extraction process has been completed')