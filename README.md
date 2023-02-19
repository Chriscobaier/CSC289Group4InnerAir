# CSC289Group4InnerAir

### Setup & Installation

```
    git clone <repo-url>
```
```
    pip install -r requirements.txt
```

### Set Environment Variables
```commandline
    export APP_SETTINGS=inner_air.config.DevelopmentConfig
    export APP_MAIL_USERNAME=c626521@gmail.com 
    export APP_MAIL_PASSWORD=nlamndkhhwpitmjz 
```

*or*
```commandline
    . ./create.sh
```
( windows )
```commandline
    set APP_SETTINGS=inner_air.config.DevelopmentConfig
    set APP_MAIL_USERNAME=c626521@gmail.com 
    set APP_MAIL_PASSWORD=nlamndkhhwpitmjz 
```

### Clean Environment
```commandline
    . ./clean.sh
```

### Running the app
```
    python main.py
```

*or*
```commandline
    make run
```

### Testing
```
    python -m pytest test_db_models.py
```
*or*
```commandline
    make test
```
### Viewing the app
```
    http://127.0.0.1:5000
```
---
### Isolated app directory
```
CSC289Group4InnerAir
├── importdata
│   ├── data.json
│   └── exercises.txt
├── inner_air
│   ├── create_and_delete.py
│   ├── dev
│   │   └── scss
│   │       ├── base.scss
│   │       ├── _buttons.scss
│   │       ├── _config.scss
│   │       ├── _form.scss
│   │       ├── _header_nav.scss
│   │       └── _hide_me.scss
│   ├── exercises
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py
│   ├── profile
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static
│   │   ├── css
│   │   │   ├── base.css
│   │   │   ├── base.css.map
│   │   │   └── styles.css
│   │   ├── ico
│   │   │   └── inner-air.ico
│   │   ├── img
│   │   │   └── inner-air.svg
│   │   └── js
│   │       └── app.js
│   ├── templates
│   │   ├── base.html
│   │   ├── errors
│   │   │   ├── 401.html
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── exercises.html
│   │   ├── main
│   │   │   └── index.html
│   │   ├── profile.html
│   │   ├── user
│   │   │   ├── confirm_email.html
│   │   │   ├── forgot.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── reset_password.html
│   │   │   ├── reset_request.html
│   │   │   └── unconfirmed.html
│   │   └── userlist.html
│   ├── user
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── token.py
│   ├── user_list
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utils
│       ├── decorators.py
│       ├── email.py
│       └── __init__.py
├── instance
│   └── inner-air-dev.db
├── main.py
├── README.md
├── requirements.txt
└── test_db_models.py
```
