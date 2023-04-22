import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user

from inner_air import db, app
from inner_air.models import User
from inner_air.user.forms import LoginForm, RegistrationForm, ForgotForm, ChangePasswordForm, ProfileForm, EmailForm, \
    SecurityAndAuthForm
from inner_air.user.token import generate_confirmation_token, confirm_token
from inner_air.utils.decorators import logout_required, check_confirmed
from inner_air.utils.email import send_email

from werkzeug.utils import secure_filename
import uuid
import os

user_bp = Blueprint(
    'user', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@user_bp.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.verify_password(attempted_password=form.password.data):
            login_user(user)
            user.updateLastLogin()
            db.session.commit()
            if user.is_confirmed:
                flash(f'Success! You are logged in as: {user.firstname}', category='success')

            if user.is_admin:
                return redirect(url_for('admin.admin'))
            return redirect(url_for('profile.profile'))
        else:
            flash('You have entered an invalid email address or password.', category='danger')
    return render_template('user/login.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            firstname=form.firstname.data,
            email=form.email.data,
            password=form.password.data,
            is_confirmed=False
        )

        if db.session.query(User).filter_by(email=form.email.data).first() is None:
            db.session.add(user)
            user.updateLastLogin()
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            html = render_template('user/confirm_email.html', confirm_url=confirm_url)
            subject = 'Please confirm your email'
            send_email(user.email, subject, html)

            login_user(user)
            flash('A confirmation email has been sent via email.', category='success')
            return redirect(url_for('user.unconfirmed'))
        else:
            flash('This email already exists. Try logging in, or register with a different email', category='danger')
    return render_template('user/register.html', form=form)


@user_bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash('Account already confirmed.', category='success')
        return redirect(url_for('main.home'))
    email = confirm_token(token)
    user = db.session.query(User).filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', category='success')
    else:
        flash('The confirmation link is invalid or has expired.', category='danger')
    return redirect(url_for('main.home'))


@user_bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_confirmed:
        return redirect(url_for('main.home'))
    return render_template('user/unconfirmed.html')


@user_bp.route('/resend')
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash('Your account has already been confirmed.', category='success')
        return redirect(url_for('main.home'))
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/confirm_email.html', confirm_url=confirm_url)
    subject = 'Please confirm your email'
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', category='success')
    return redirect(url_for('user.unconfirmed'))


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you\'ve been logged out', category='info')
    return redirect(url_for('main.home'))


@user_bp.route('/forgot', methods=['GET', 'POST'])
@logout_required
def forgot():
    form = ForgotForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is not None:
            token = generate_confirmation_token(user.email)
            user.password_reset_token = token
            db.session.commit()

            reset_url = url_for('user.reset_password', token=token, _external=True)
            html = render_template('user/reset_request.html', email=user.email, reset_url=reset_url)
            subject = 'Reset your password'
            send_email(user.email, subject, html)
            return render_template('user/confirm_reset_request.html', email=user.email)
        else:
            flash('This email is not registered', category='danger')
    return render_template('user/forgot.html', form=form)


@user_bp.route('/forgot/<token>', methods=['GET', 'POST'])
@logout_required
def reset_password(token):
    email = confirm_token(token)
    user = db.session.query(User).filter_by(email=email).first_or_404()

    if user.password_reset_token is not None:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(email=email).first()
            if user:
                user.password = form.password.data
                user.password_reset_token = None
                db.session.commit()

                flash('Password changed successfully.', category='success')
                return redirect(url_for('main.home'))
            else:
                flash('Password change was unsuccessful.', category='danger')
                return redirect(url_for('main.home'))
        else:
            flash('You can now change your password.', category='success')
            return render_template('user/reset_password.html', form=form)
    else:
        flash('Can not reset the password, try again.', category='danger')
    return redirect(url_for('main.home'))


"""""
    update user profile
"""""


@user_bp.route('/settings/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    form = ProfileForm()
    user_profile = db.session.query(User).get_or_404(id)

    if user_profile.is_authenticated and current_user.is_admin:
        print('is admin')
    elif user_profile.is_authenticated and not current_user.is_admin:
        if user_profile != current_user:
            abort(403)
    if user_profile.is_authenticated:
        form.anonymous_mode.checked = user_profile.is_anonymous

    if form.validate_on_submit():

        user_profile.firstname = request.form['firstname']
        print(form.anonymous_mode.data)
        user_profile.is_anonymous = form.anonymous_mode.data

        if request.files['profile_picture']:
            user_profile.profile_picture = request.files['profile_picture']

            picture_fname = secure_filename(user_profile.profile_picture.filename)
            picture_name = '-'.join([str(uuid.uuid4()), str(picture_fname)])
            user_profile.profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_name))
            user_profile.profile_picture = picture_name
            try:
                db.session.commit()
                flash('Your profile has been updated successfully.', category='success')
                return render_template('user/profile.html', form=form, user_profile=user_profile)
            except Exception:
                flash('An error occurred...try again.', category='danger')
                return render_template('user/profile.html', form=form, user_profile=user_profile)
        else:
            db.session.commit()
            flash('Your profile has been updated successfully.', category='success')
            form.anonymous_mode.checked = user_profile.is_anonymous

            return render_template('user/profile.html', form=form, user_profile=user_profile)
    else:
        return render_template('user/profile.html', form=form, user_profile=user_profile)


@user_bp.route('/settings/emails/<int:id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def emails(id):
    form = EmailForm()
    user_email = db.session.query(User).get_or_404(id)

    if user_email.is_authenticated and current_user.is_admin:
        print('is admin')
    elif user_email.is_authenticated and not current_user.is_admin:
        if user_email != current_user:
            abort(403)

    if form.validate_on_submit():
        user_email.email = request.form['email']

        if current_user.is_admin:
            user_email.is_confirmed = True
        else:
            user_email.is_confirmed = False

        try:
            db.session.commit()
            token = generate_confirmation_token(user_email.email)
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            html = render_template('user/confirm_email.html', confirm_url=confirm_url)
            subject = 'Please confirm your email'
            send_email(user_email.email, subject, html)

            flash('Your email has been updated successfully.', category='success')
            return render_template('user/email_settings.html', form=form, user_email=user_email)
        except Exception:
            flash('An error occurred...try again.', category='danger')
            return render_template('user/email_settings.html', form=form, user_email=user_email)
    else:
        return render_template('user/email_settings.html', form=form, user_email=user_email)


@user_bp.route('/settings/security/<int:id>', methods=['GET', 'POST'])
@login_required
def security(id):
    form = SecurityAndAuthForm()
    user_password = db.session.query(User).get_or_404(id)

    if user_password.is_authenticated and current_user.is_admin:
        print('is admin')
    elif user_password.is_authenticated and not current_user.is_admin:
        if user_password != current_user:
            abort(403)

    if form.validate_on_submit():
        user_password.password = request.form['password']
        if user_password:
            user_password.password = form.password.data
            db.session.commit()
            flash('Password changed successfully.', category='success')
            return redirect(url_for('user.security', id=user_password.id))
        else:
            flash('Can not change the password, try again.', category='danger')
            return redirect(url_for('user.security', id=user_password.id))
    return render_template('user/account_security.html', form=form)
