from flask import render_template, flash, redirect,url_for, redirect, request
from statsmodels.stats.power import TTestPower, TTestIndPower
import math as m

def powerFunc(effect,alpha,power,nobs,test):
    
    print("test")

    if test == 'independent':
        analysis = TTestPower()
        print("test")
        # this is where the program brakes, the parameters are right, I'm not sure why this is not working
        result = analysis.solve_power(effect_size=None,nobs=8,alpha=0.05,power=0.8, alternative="two-sided") 
        print("test")
    elif test == 'paired':
        analysis = TTestIndPower()
        result = analysis.solve_power(effect_size=effect,nobs=nobs,alpha=alpha,power=power, ratio = 1, alternative='two-sided')

    result = str(result)

    if effect is None:
        print("\nThe Effect size should be %.2f\n" % result)
        flash("The Effect size should be %.2f\n" % result)
    elif power is None:
        print('The power is {}'.format(m.ceil(result)))
        flash("The power is {}".format(m.ceil(result)))
    elif nobs is None:
        print("The sample size should be %.2f\n" % result)
        flash("The sample size should be %.2f\n" % result)
