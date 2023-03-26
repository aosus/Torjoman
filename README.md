# Torjoman | تُرجمان
Torjoman aims to make translating more accessible to general users, by translating inside the users favourite Platforms, be it chat or a website or any other platform.
So translations can be crowd sourced from even more people, which will result in more recognizable translations for normal users.

it's designed to be modular, so anyone can create a plug-in to support any new platform, using the Torjoman Plug-in API.

The project is currently in the planing phase, and you can find the documentation and the plan here(in Arabic only currently):
https://torjoman.aosus.dev

## Flowchart

https://torjoman.aosus.dev/project-plan/#_3

## How to run
1. Install dependencies Using poetry
      ```shell
      poetry install --no-root
      ```
2. Create `.env` file
   Create a .env file in `project` and fill it with the following data
   ```
   SECRET_KEY=
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_USER=
   DATABASE_PASSWORD=
   DATABASE_NAME=
   JWT_SIGNING_KEY=
   HOST_NAME=
   ```
   write your hostname without `www.`, like `torjoman.com` or `torjoman.aosus.org`.
3. Create superuser account, Run ```python manage.py createsuperuser```
4. Run ```python manage.py migrate```
5. Static Files (css, js, images)
      1. Run ```python manage.py collectstatic```
      2. serve static folder, see [here](https://docs.djangoproject.com/en/4.1/howto/static-files/deployment/)
6. Run server. see [Here](https://docs.djangoproject.com/en/4.1/howto/deployment/). you can use the following command **just for testing**
   ```shell
   poetry run ./manage.py runserver           
   ```




## License
Torjoman is licensed under the AGPLv3

![license](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
