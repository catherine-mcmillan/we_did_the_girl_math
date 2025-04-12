from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.user import User
from app.forms.auth_forms import LoginForm, RegistrationForm
from urllib.parse import urlparse
import requests

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/facebook/callback', methods=['POST'])
def facebook_callback():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Invalid request format'}), 400
    
    data = request.get_json()
    access_token = data.get('accessToken')
    user_info = data.get('userInfo')
    
    if not access_token or not user_info:
        return jsonify({'success': False, 'error': 'Missing required data'}), 400
    
    # Verify the access token with Facebook
    verify_url = f'https://graph.facebook.com/debug_token?input_token={access_token}&access_token={current_app.config["FACEBOOK_CLIENT_ID"]}|{current_app.config["FACEBOOK_CLIENT_SECRET"]}'
    verify_response = requests.get(verify_url)
    
    if verify_response.status_code != 200:
        return jsonify({'success': False, 'error': 'Invalid access token'}), 401
    
    # Check if user already exists
    user = User.query.filter_by(facebook_id=user_info['id']).first()
    
    if user is None:
        # Create new user
        user = User(
            username=user_info['name'],
            email=user_info.get('email', f"{user_info['id']}@facebook.com"),
            facebook_id=user_info['id']
        )
        db.session.add(user)
        db.session.commit()
        flash('Welcome! Your account has been created.')
    else:
        flash('Welcome back!')
    
    # Log the user in
    login_user(user, remember=True)
    
    return jsonify({
        'success': True,
        'message': 'Successfully logged in',
        'redirect': url_for('main.index')
    })

# TODO: Add routes for Facebook OAuth integration