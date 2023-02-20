#!/usr/bin/env bash

function clean_env() {
    unset APP_SETTINGS
    unset APP_MAIL_USERNAME
    unset APP_MAIL_PASSWORD
}

# function call
clean_env
echo 'environment variables have been unset.'

rm -rfv instance/*.db