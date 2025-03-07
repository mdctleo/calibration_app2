from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class powerForm(FlaskForm):
    effect = FloatField('Effect', default=None , validators=[DataRequired()])
    nobs = IntegerField('nobs', default=None, validators=[DataRequired()]) # nobs = number of observations
    alpha = SelectField('Alpha', choices=[(0.05, '0.05'), (0.01, '0.01')]) 
    power = FloatField('Power', default=0.8, validators=[DataRequired()])
    test = SelectField('Test', choices=[('independent', 'independent samples'), ('paired', 'paired samples')])
    alternative = SelectField('Alternative', choices=[('two-sided', 'two-sided'), ('larger', 'larger'), ('smaller', 'smaller')])
    submit2 = SubmitField('Submit')
