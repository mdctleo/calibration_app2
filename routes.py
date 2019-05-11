from app import app
from flask import render_template, flash, redirect,url_for, redirect, request

from forms import LoginForm, powerForm
from flask_login import current_user, login_user,logout_user, login_required
from user.Model import User

# TODO: Refactor this


@app.route('/')
@app.route('/index')
@login_required
def index():
    print("Got here")
    text = {'content':'Home'}
    return render_template('index.html',title='medphys',text=text)

@app.route('/gcbiodi')
def gc_biodi():
    text = {'content':'Hello world biodi'}
    user = {'username':'Carlos'}

    return render_template('gcbiodi.html',text=text,user=user)

# connecting to power.html
@app.route('/power', methods=['GET', 'POST'])
def power():
    form = powerForm()

    # Detting the default value of alpha as 0.05
    if request.method == 'GET':
        form.alpha.default = 0.05
        form.process()


    if (request.method == 'POST'):
        effect = request.form['effect']
        alpha = request.form['alpha']
        power = request.form['power']
        test = request.form['test']

        # output the user input on the shell
        print("\nEffect: " + effect + "     Alpha: " + alpha + "    Power: " + power + "    Test: " + test +"\n")

        # output the user input on the webpage
        flash("\n Effect: " + effect + "   Alpha: " + alpha + "   Power: " + power + "   Test: " + test)


    # if (form.validate_on_submit()):
    #     flash(' Effect: ' + effect + '\n Alpha: ' + alpha + '\n Power: ' + power + '\n Test: ' + test)
    #     flash('Alpha' + alpha)
    #     flash('Power ' + power)
    #     flash('Test' + test)

    return render_template('power.html', form=form)


'''
# https://pythonspot.com/flask-web-forms/
# https://www.reddit.com/r/flask/comments/a5hxdi/how_to_give_a_drop_down_list_a_selected_value/
'''

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    print("got here")
    if form.validate_on_submit():
        print("form validated")
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        print(form.password.data)
        if user is None or not user.check_password(form.password.data):
            print("log in failed")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print('logged in successfully')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form,user='test')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))