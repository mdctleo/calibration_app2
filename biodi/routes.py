from flask import render_template, flash, redirect,url_for
from biodi import app_biodi
from biodi.forms import LoginForm
from flask_login import current_user, login_user,logout_user, login_required
from biodi.models import User

@app_biodi.route('/')
@app_biodi.route('/index')
@login_required
def index():
    text = {'content':'Home'} 
    return render_template('index.html',title='medphys',text=text)

@app_biodi.route('/gcbiodi')
def gc_biodi():
    text = {'content':'Hello world biodi'}
    user = {'username':'Carlos'}

    return render_template('gcbiodi.html',text=text,user=user)

@app_biodi.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))        
    return render_template('login.html', title='Sign In', form=form,user='test')


@app_biodi.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))