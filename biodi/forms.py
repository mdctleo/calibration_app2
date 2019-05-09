from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class powerForm(FlaskForm):
    effect = FloatField('Effect', validators=[DataRequired()])
    alpha = SelectField('Alpha', choices=[(0.05, '0.05'), (0.01, '0.01')])
    power = FloatField('Power', default=0.8, validators=[DataRequired()])
    test = SelectField('Test', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])
    submit2 = SubmitField('Submit')
