from app import app
from flask import render_template, flash, redirect, url_for, redirect, request
from statistics_app import bp
from statistics_app.Model import StatisticFormSchema, StatisticFormResponseSchema
from forms import LoginForm, powerForm
from flask_login import current_user, login_user, logout_user, login_required
from user.Model import User
from statsmodels.stats.power import TTestPower, TTestIndPower
from methods.statistics import *
from methods.statistics import powerFunc
from marshmallow import ValidationError
from response.response import StandardResponse, StandardResponseSchema
from flask import jsonify


def calcEffect(statisticFormDict):
    effect = None
    nobs = statisticFormDict['nobs']
    power = statisticFormDict['power']
    alpha = statisticFormDict['alpha']
    test = statisticFormDict['test']
    alternative = statisticFormDict['alternative']

    return powerFunc(effect, float(alpha), float(power), int(nobs), test, alternative)

def calcNobs(statisticFormDict):
    nobs = None
    effect = statisticFormDict['effect']
    power = statisticFormDict['power']
    alpha = statisticFormDict['alpha']
    test = statisticFormDict['test']
    alternative = statisticFormDict['alternative']

    return powerFunc(effect, float(alpha), float(power), nobs, test, alternative)

def calcPower(statisticFormDict):
    power = None
    effect = statisticFormDict['effect']
    nobs = statisticFormDict['nobs']
    alpha = statisticFormDict['alpha']
    test = statisticFormDict['test']
    alternative = statisticFormDict['alternative']

    return powerFunc(float(effect), float(alpha), power, int(nobs), test, alternative)

def calcPowerGraph(statisticFormDict):
    power = None
    effect = statisticFormDict['effect']
    nobs = statisticFormDict['nobs']
    alpha = statisticFormDict['alpha']
    test = statisticFormDict['test']
    alternative = statisticFormDict['alternative']
    plot, table = createLineGraphAndTable(int(nobs), float(alpha), power, alternative, test)

    return plot, table




# TODO: Refactor this
@bp.route('/effectCalc', methods=['GET'])
def effectCalc():
    if request.method == 'GET':
        nobs = request.args.get('nobs')
        power = request.args.get('power')
        alpha = request.args.get('alpha')
        test = request.args.get('test')
        alternative = request.args.get('alternative')
        try:
            statisticFormDict = StatisticFormSchema().load(
                {'nobs': nobs, 'power': power, 'alpha': alpha, 'test': test, 'alternative': alternative}
            )
            result= calcEffect(statisticFormDict)
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except Exception as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = StatisticFormResponseSchema().dump({'result': result})
        return jsonify(response), 200


@bp.route('/nobsCalc', methods=['GET'])
def nobsCalc():
    if request.method == 'GET':
        effect = request.args.get('effect')
        alpha = request.args.get('alpha')
        power = request.args.get('power')
        test = request.args.get('test')
        alternative = request.args.get('alternative')

        try:
            statisticFormDict = StatisticFormSchema().load(
                {'effect': effect, 'power': power, 'alpha': alpha, 'test': test, 'alternative': alternative}
            )
            result = calcNobs(statisticFormDict)
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except Exception as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = StatisticFormResponseSchema().dump({'result': result})
        return jsonify(response), 200


@bp.route('/powerCalc', methods=['GET'])
def powerCalc():
    if request.method == 'GET':
        effect = request.args.get('effect')
        nobs = request.args.get('nobs')
        alpha = request.args.get('alpha')
        test = request.args.get('test')
        alternative = request.args.get('alternative')

        try:
            statisticFormDict = StatisticFormSchema().load(
                {'effect': effect, 'nobs': nobs, 'alpha': alpha, 'test': test, 'alternative': alternative}
            )
            result = calcPower(statisticFormDict)
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except Exception as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = StatisticFormResponseSchema().dump({'result': result})
        return jsonify(response), 200


@bp.route('/powerCalcGraph', methods=['GET'])
def powerCalcGraph():
    if request.method == 'GET':
        effect = request.args.get('effect')
        nobs = request.args.get('nobs')
        alpha = request.args.get('alpha')
        test = request.args.get('test')
        alternative = request.args.get('alternative')

        try:
            statisticFormDict = StatisticFormSchema().load(
                {'effect': effect, 'nobs': nobs, 'alpha': alpha, 'test': test, 'alternative': alternative}
            )
            plot, table = calcPowerGraph(statisticFormDict)
        except Exception as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

    response = plot
    return response, 200

@bp.route('/powerCalcTable', methods=['GET'])
def powerCalcTable():
    if request.method == 'GET':
        effect = request.args.get('effect')
        nobs = request.args.get('nobs')
        alpha = request.args.get('alpha')
        test = request.args.get('test')
        alternative = request.args.get('alternative')

        try:
            statisticFormDict = StatisticFormSchema().load(
                {'effect': effect, 'nobs': nobs, 'alpha': alpha, 'test': test, 'alternative': alternative}
            )
            plot, table = calcPowerGraph(statisticFormDict)
        except Exception as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

    response = table
    return response, 200