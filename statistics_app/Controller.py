from app import app
from flask import render_template, flash, redirect, url_for, redirect, request
from statistics_app import bp
from statistics_app.Model import StatisticFormSchema, StatisticFormResponseSchema
from forms import LoginForm, powerForm
from flask_login import current_user, login_user, logout_user, login_required
from user.Model import User
from statsmodels.stats.power import TTestPower, TTestIndPower
from methods.statistics import *
from functions.functions import powerFunc
from marshmallow import ValidationError
from response.response import StandardResponse, StandardResponseSchema
from flask import jsonify


def calcEffect(statisticFormDict):
    effect = None
    nobs = statisticFormDict['input0']
    power = statisticFormDict['power']
    alpha = statisticFormDict['alpha']
    test = statisticFormDict['test']
    alternative = statisticFormDict['alternative']

    return powerFunc(effect, float(alpha), float(power), int(nobs), test, alternative)




# TODO: Refactor this
@bp.route('/effectCalc', methods=['GET'])
def effectCalc():
    # form = powerForm()

    # feature = 'Bar'
    # bar = create_plot(feature)

    # Setting the default value of alpha as 0.05
    if request.method == 'GET':
        # form.alpha.default = 0.05
        # form.process()
        input0 = request.args.get('input0')
        input1 = request.args.get('input1')
        alpha = request.args.get('alpha')
        test = request.args.get('test')
        alternative = request.args.get('alternative')
        try:
            statisticFormDict = StatisticFormSchema().load(
                {'input0': input0, 'input1': input1, 'alpha': alpha, 'test': test, 'alternative': alternative}
            )
            result = calcEffect(statisticFormDict)
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400

        response = StatisticFormResponseSchema().dump(result)
        return jsonify(response), 200








    if (request.method == 'POST'):
        effect = None
        nobs = request.form['nobs']
        alpha = request.form['alpha']
        power = request.form['power']
        test = request.form['test']
        alternative = request.form['alternative']

        # output the user input on the shell
        # print("\nnobs: " + nobs  + "    Alpha: " +  alpha  + "     Power: " + power  + "   Test: " + test + "   Alternative: " + alternative + "\n")

        powerFunc(effect, float(alpha), float(power), int(nobs), test, alternative)

    return render_template('powerForms/effectCalc.html', form=form)


@bp.route('/nobsCalc', methods=['GET'])
def nobsCalc():
    form = powerForm()

    feature = 'Bar'
    # bar = create_plot(feature)

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

        powerFunc(float(effect), float(alpha), float(power), nobs, test, alternative)


    return render_template('powerForms/nobsCalc.html')


@bp.route('/powerCalc', methods=['GET'])
def powerCalc():
    form = powerForm()

    feature = 'Line'
    # plot = create_plot(feature)
    # table = createTable()

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

        # output the user input on the shell
        # print("\nEffect: " + effect  + "    nobs: " + nobs  + "    Alpha: " +  alpha  + "   Test: " + test +"\n")

        powerFunc(float(effect), float(alpha), power, int(nobs), test, alternative)
        # plot, table = createLineGraphAndTable(int(nobs), float(alpha), power, alternative, test)

    return render_template('powerForms/powerCalc.html')
