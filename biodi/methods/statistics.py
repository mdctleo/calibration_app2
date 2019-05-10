from flask import render_template, flash, redirect,url_for, redirect, request
from statsmodels.stats.power import TTestPower, TTestIndPower


def powerFunc(effect,alpha,power,nobs,test):
    
    if test == 'independent':
        analysis = TTestPower()
    elif test == 'paired':
        analysis = TTestIndPower()
    
    # if (effect is None):
    #     effect = None
    # if (nobs is None):
    #     nobs = None
    # if (power is None):
    #     power = None


    result = analysis.solve_power(effect_size=effect,nobs=nobs,alpha=alpha,power=power)

    if not effect:
        print('The effect size is {}'.format(result))
        flash("The effect size is " + result)
    elif not power:
        print('The power is {}'.format(result))
        flash("The power is " + result)
    elif not nobs:
        print('The sample size should be {}'.format(result))
        flash("The sample size should be " + result)
