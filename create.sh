#!/usr/bin/env bash

function set_env() {
    export APP_SETTINGS=inner_air.config.DevelopmentConfig
    export APP_MAIL_USERNAME=c626521@gmail.com
    export APP_MAIL_PASSWORD=nlamndkhhwpitmjz
}

# function call
set_env
echo 'environment variables have been set.'
