#!/usr/bin/env bash

function set_env() {
    set APP_SETTINGS=inner_air.config.DevelopmentConfig
    set APP_MAIL_USERNAME=c626521@gmail.com
    set APP_MAIL_PASSWORD=nlamndkhhwpitmjz
}

function export_env() {
    export APP_SETTINGS=inner_air.config.DevelopmentConfig
    export APP_MAIL_USERNAME=c626521@gmail.com
    export APP_MAIL_PASSWORD=nlamndkhhwpitmjz
}

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "-----linux------"
    export_env
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "-----Mac OSX-----"
    export_env
else
    echo "-----Windows----"
    set_env
fi

echo 'environment variables have been set.'
