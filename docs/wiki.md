
### Set Environment Variables
---
***Create a file named ```.env``` in the root directory and add the following content there:***
```dotenv
#####################
# BASE CONFIG       #
#####################
DB_NAME=<db_name.db>
APP_SETTINGS=inner_air.config.DevelopmentConfig
APP_TESTING_SETTINGS=inner_air.config.TestingConfig
SECRET_KEY=<your_secret_key>

#####################
# PROFILE PIC       #
#####################
HOST=<url>
USR=<your_username>
PASSWD=<your_password>

#####################
# PROFILE PIC       #
#####################
UPLOAD_FOLDER=inner_air/user/static/img/profile_pics/

#####################
# MAIL SETTINGS     #
#####################
SECURITY_PASSWORD_SALT=<your_security_passwd>
APP_MAIL_DEFAULT_SENDER=<your_email>
APP_MAIL_USERNAME=<your_email>
APP_MAIL_PASSWORD=<your_passwd>
```
***Run the following command to export all the environment variables from the .env file:***
```commandline
    source .env
```

### Run the App
---
***Create admin account***
```commandline
  python wsgi.py create_admin
```
***or***
```commandline
  make admin
```
***Running the app***
```commandline
    python wsgi.py run --debug
```
***or***
```commandline
    make
```
***Running tests***
```commandline
    python -m pytest tests
```
***or***
```commandline
   make test
```
***Viewing the app***
````commandline
    http://127.0.0.1:5000
````

## App Structure with Blueprints
```commandline

```