# from translate.models import Word as TWord, Translate as TTranslate
from .models import PullRequest
from github import Github
import json
import os
from pathlib import Path
from django.conf import settings


account = Github(os.environ.get("GITHUB_ACCOUNT_TOKEN"))
dictionary_repo = account.get_repo(os.environ.get('JSON_REPO'))
local_json_file: Path = (settings.BASE_DIR / 'local_dictionary.json').resolve()

if not local_json_file.exists():
  raise Exception("Please run 'python3 project/prepare-project.py' before run Torjoman for the first time")

def check_for_update_json():
  file = dictionary_repo.get_contents(os.environ.get('JSON_FILE'))
  repo_file_json = json.loads(file.decoded_content)
  old_file_json = json.loads(local_json_file.read_text())
  if repo_file_json == old_file_json:
    return
  else:
    print('Files Are not the same')
    with open(str(local_json_file), 'w') as f:
      json.dump(repo_file_json, f, ensure_ascii=False, indent=2)
    update_source(repo_file_json)


def push(_payload: dict):
  print("New Push Event")
  check_for_update_json()
  print("Finished Push Event")
