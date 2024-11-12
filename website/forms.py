from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from website.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(), Length(min=5, max=20)])
  password = PasswordField('Password',validators=[DataRequired(), Length(min=5, max=20)])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Username already exists! Please choose a different one!')
    
class LoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(), Length(min=5, max=20)])
  password = PasswordField('Password',validators=[DataRequired(), Length(min=5, max=20)])
  submit = SubmitField('Login')

