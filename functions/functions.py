from flask import render_template, flash, redirect,url_for, redirect, request
from statsmodels.stats.power import TTestPower, TTestIndPower


def powerFunc(effect_size, alpha, power, nobs, test, alternative):

    # alternative = 'two-sided'
    print(alpha)
    print(power)
    print(nobs)
    print("test")

    if (test == 'independent'):
        analysis = TTestPower()
        result = analysis.solve_power(effect_size=effect_size, nobs=nobs, alpha=alpha, power=power, alternative=alternative)
    elif (test == 'paired'):
        analysis = TTestIndPower()
        result = analysis.solve_power(effect_size=effect_size, nobs1=nobs, alpha=alpha, power=power, ratio=1, alternative=alternative)

    if effect_size is None:
        word = "effect size"
    elif power is None:
        word = "power"
    elif nobs is None:
        word = "sample size"

    result = str(result)

    # return resultString
    flash("The " + word + " should be " + result)