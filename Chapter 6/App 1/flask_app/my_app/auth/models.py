from werkzueg.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo 
from my_app import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    pwdhash = db.Column(db.String())
    
    def __init__(self, username, password):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
        

class RegistraionForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField(
        'Password', [
            InputRequired(), EqualTo('confirm', message='Password must match')
        ]
    )
    confirm = PasswordField('Repeat Password', [InputRequired])
    
class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])