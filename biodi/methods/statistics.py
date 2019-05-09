from statsmodels.stats.power import TTestPower, TTestIndPower


def power(effect,alpha,power,nobs,test)
    
    if test == 'independent':
        analysis = TTestPower()
    elif test == 'paired':
        analysis = TTestIndPower()


    
    result = analysis.solve_power(effect_size=effect,nobs=nobs,alpha=alpha,power=power)

    if not effect:
        print('The effect size is {}'.format(result))
    elif not power:
        print('The power is {}'.format(result))
    elif not nobs:
        print('The sample size should be {}'.format(result))
