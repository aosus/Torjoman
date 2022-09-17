# Torjoman | تُرجمان
Torjoman aims to make translating more accessible to general users, by translating inside the users favourite Platforms, be it chat or a website or any other platform.
So translations can be crowd sourced from even more people, which will result in more recognizable translations for normal users.

it's designed to be modular, so anyone can create a plug-in to support any new platform, using the Torjoman Plug-in API.

The project is currently in the planing phase, and you can find the documentation and the plan here(in Arabic only currently):
https://torjoman.aosus.dev

## Flowchart

https://torjoman.aosus.dev/project-plan/#_3

## How to run
1. Install dependencies
   * Using pipenv
    	```pipenv install```
   * Using pip
		```pip install -r requirements.txt```
2. Create `.env` file
   Create a .env file in `project` and fill it with the following data
   ```
   SECRET_KEY=
   GITHUB_WEBHOOK_KEY=
   DATABASE_NAME=
   DATABASE_USER=
   DATABASE_PASSWORD=
   DATABASE_HOST=
   DATABASE_PORT=5432
   JSON_REPO=GtihubUser/REPO
   JSON_FILE=PathToJsonFileInYourRepo
   ```
   json file format example can be found in `json-example.json`
3. Run ```python project/prepare-project.py```
4. Create superuser account, Run ```python manage.py createsuperuser```
5. Run ```python manage.py migrate```
6. Run server. see [Here](https://docs.djangoproject.com/en/4.1/howto/deployment/)
7. Wait for the server to finish extracting data from the json file. It will print `The first data extraction process has been completed` when it finishes
8. Set your github webhook payload url to `https://your-domain.com/api/webhook/`. Don't forget to set webhook key
9. Add some platfroms endpoints to deal with from `htStps://your-domain.com/admin`



## License
Torjoman is licensed under the AGPLv3

![license](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
