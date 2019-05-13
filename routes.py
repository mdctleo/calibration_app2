from app import app
from flask import render_template, flash, redirect, url_for, redirect, request

from forms import LoginForm, powerForm
from flask_login import current_user, login_user, logout_user, login_required
from user.Model import User
from statsmodels.stats.power import TTestPower, TTestIndPower
from functions.functions import powerFunc


# TODO: Refactor this


@app.route('/')
@app.route('/index')
@login_required
def index():
    print("Got here")
    text = {'content': 'Home'}
    return render_template('index.html', title='medphys', text=text)


@app.route('/gcbiodi')
def gc_biodi():
    text = {'content': 'Hello world biodi'}
    user = {'username': 'Carlos'}

    return render_template('gcbiodi.html', text=text, user=user)


# connecting to power.html
@app.route('/power')  # , methods=['GET', 'POST'])
def power():
    form = powerForm()

    return render_template('power.html', form=form)


@app.route('/effectCalc', methods=['GET', 'POST'])
def effectCalc():
    form = powerForm()

    # Setting the default value of alpha as 0.05
    if request.method == 'GET':
        form.alpha.default = 0.05
        form.process()

    if (request.method == 'POST'):
        effect = None
        nobs = request.form['nobs']
        alpha = request.form['alpha']
        power = request.form['power']
        test = request.form['test']
        alternative = request.form['alternative']

        # # output the user input on the shell
        print(
            "\nnobs: " + nobs + "    Alpha: " + alpha + "     Power: " + power + "   Test: " + test + "   Alternative: " + alternative + "\n")

        nobs = int(nobs)
        alpha = float(alpha)
        power = float(power)

        powerFunc(effect, alpha, power, nobs, test, alternative)

    return render_template('powerForms/effectCalc.html', form=form)


@app.route('/nobsCalc', methods=['GET', 'POST'])
def nobsCalc():
    form = powerForm()

    # Setting the default value of alpha as 0.05
    if request.method == 'GET':
        form.alpha.default = 0.05
        form.process()

    if (request.method == 'POST'):
        effect = request.form['effect']
        nobs = None
        alpha = request.form['alpha']
        power = request.form['power']
        test = request.form['test']
        alternative = request.form['alternative']

        effect = float(effect)
        alpha = float(alpha)
        power = float(power)

        powerFunc(effect, alpha, power, nobs, test, alternative)

    return render_template('powerForms/nobsCalc.html', form=form)


@app.route('/powerCalc', methods=['GET', 'POST'])
def powerCalc():
    form = powerForm()

    # Setting the default value of alpha as 0.05
    if request.method == 'GET':
        form.alpha.default = 0.05
        form.process()

    if (request.method == 'POST'):
        effect = request.form['effect']
        nobs = request.form['nobs']
        alpha = request.form['alpha']
        power = None
        test = request.form['test']
        alternative = request.form['alternative']

        #  # output the user input on the shell
        print("\nEffect: " + effect + "    nobs: " + nobs + "    Alpha: " + alpha + "   Test: " + test + "\n")

        effect = float(effect)
        nobs = float(nobs)
        alpha = float(alpha)

        powerFunc(effect, alpha, power, nobs, test, alternative)

    return render_template('powerForms/powerCalc.html', form=form)


'''
# https://pythonspot.com/flask-web-forms/
# https://www.reddit.com/r/flask/comments/a5hxdi/how_to_give_a_drop_down_list_a_selected_value/
'''


@app.route('/login', methods=['GET', 'POST'])
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
    return render_template('login.html', title='Sign In', form=form, user='test')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
