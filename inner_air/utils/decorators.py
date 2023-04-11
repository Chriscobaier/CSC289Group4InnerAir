import inspect
from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already authenticated.', category='info')
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)

    return decorated_function


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash('Please confirm your account!', category='warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def def_params(func):
    sig = inspect.signature(func)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        # print(f'{bound.arguments}')
        return func(*args, **kwargs)

    return decorated_function
