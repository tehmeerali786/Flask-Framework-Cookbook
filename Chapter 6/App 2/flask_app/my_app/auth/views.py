from flask import request, render_template, flash, redirect, url_for, session, Blueprint, g
from flask_login import current_user, login_user, logout_user, login_required
from my_app import app, db, login_manager
from my_app.auth.models import User, RegistrationForm, LoginForm 
auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.before_request 
def get_current_user():
    g.user = current_user



@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect( url_for('auth.home') )
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(
            User.username.like('%' + username    +  '%')
        ).first()
        
        if existing_username:
            
            flash(
                'This username has been already taken. Try another one.', 'warning'
            )
            
            return render_template('register.html', form=form)
        
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        
        flash('You are now registered. Please login.', 'success')
        return redirect( url_for('auth.login') )
    
    if form.errors:
        flash(form.errors, 'danger')
        
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect( url_for('auth.home') )
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)
        login_user(existing_user)
        flash('You have successfully logged in.', 'success')
        return redirect( url_for('auth.home') )
    
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for('auth.home') )