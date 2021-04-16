# Instructions to Run Flask Backend Outside Docker Container

In the client folder:

```bash
npm build
```

In the server folder create a instance folder and config.py file inside the instance folder at the same level as the flask_api folder. Add the DATABASE_SECRET_KEY, DATABASE_USERNAME and DATABASE_URL to the config.py file.

In the server folder run the following commands:

```bash
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt
export FLASK_APP=flask_api
flask run
```

Or on Windows (command prompt):

```bash
> py -3 -m venv venv
> venv\Scripts\activate
> py -3 -m pip install -r requirements.txt
> set FLASK_APP=flask_api
> set FLASK_ENV=development
> flask run
```

References:

- https://flask.palletsprojects.com/en/1.1.x/installation/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/#run-the-application
