from flask import render_template, flash, redirect,url_for, redirect, request
from statsmodels.stats.power import TTestPower, TTestIndPower
import math as m

# import plotly
# import plotly.graph_objs as go
import numpy as np
import pandas as pd
import json


def powerFunc(effect,alpha,power,nobs,test, alternative):
    
    # print("test")

    if test == 'independent':
        analysis = TTestPower()
        # print("test")
        # this is where the program brakes, the parameters are right, I'm not sure why this is not working
        result = analysis.solve_power(effect_size=effect,nobs=nobs,alpha=alpha,power=power, alternative=alternative) 
        # print("test")
    elif test == 'paired':
        analysis = TTestIndPower()
        result = analysis.solve_power(effect_size=effect,nobs1=nobs,alpha=alpha,power=power, alternative=alternative)

    # result = str(result)

    return result

    # if effect is None:
    #     print("\nThe Effect size should be %.2f\n" % result)
    #     flash("The Effect size should be %.2f\n" % result)
    # elif nobs is None:
    #     print('\nThe Sample Size is should be {}'.format(m.ceil(result)))
    #     flash("The Sample Size is should be {}".format(m.ceil(result)))
    # elif power is None:
    #     print("\nThe Power should be %.2f\n" % result)
    #     flash("The Power should be %.2f\n" % result)


# def create_plot(feature):
#     if (feature == 'Bar'):
#         trace1 = go.Bar(
#             x = [1, 2, 3],
#             y = [4, 1, 2],
#             name = 'SF'
#         )
#         trace2 = go.Bar(
#             x = [1, 2, 3],
#             y = [2, 4, 5],
#             name = 'Montreal'
#         )
#
#         data = [trace1, trace2]
#     elif (feature == 'Line'):
#         N = 500
#         randomX = np.linspace(0, 1, N)
#         randomY = np.random.randn(N)
#
#         trace = go.Scatter(
#             x = randomX,
#             y = randomY
#         )
#         data = [trace]
#
#
#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
#
#
# # create table
# def createTable():
#     trace = go.Table(
#         header=dict(values=['Effect Size', 'Power N_1', 'Power N_2', 'Power N_3']),
#         cells=dict(values=[[100, 90, 80, 90],
#                            [100, 90, 80, 90],
#                            [100, 90, 80, 90],
#                            [95, 85, 75, 95]]))
#
#     data = [trace]
#
#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
#
#
#
# # Plot the data into a graph and table
# def createLineGraphAndTable(nobs, alpha, power, alternative, test):
#     nobsArr = [nobs, nobs-2, nobs+2]
#     es = np.arange(0, 5.1, 0.1)
#     data = []
#     newArr = []
#     resultArr = [es]
#     nameArr = ['Effect Size']
#
#     if (test == 'independent'):
#         # Putting results in array
#         for i in range(len(nobsArr)):
#             # X-azis = es, Y-axis = result
#             result = TTestPower().solve_power(effect_size=es, nobs=nobsArr[i], alpha=alpha, power=power, alternative=alternative)
#             newArr.append(result)
#
#
#     elif (test == 'paired'):
#         # Putting results in array
#         for i in range(len(nobsArr)):
#             # X-azis = es, Y-axis = result
#             result = TTestIndPower().solve_power(effect_size=es, nobs1=nobsArr[i], alpha=alpha, power=power, alternative=alternative)
#             newArr.append(result)
#
#     # plot the data into the line graph
#     for i in range(len(newArr)):
#             trace = go.Scatter(
#                 x = es,
#                 y = newArr[i],
#                 mode = 'lines',
#                 name = 'nobs: ' + str(nobsArr[i])
#             )
#             data.append(trace)
#
#     # Adding title
#     layout = dict(title = 'Need Title',
#                   xaxis = dict(title='Effect Size'),
#                   yaxis = dict(title='Power'),
#                   )
#
#     graph = dict(data = data, layout=layout)
#
#     # lineGraph = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     lineGraph = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
#
#     ## create Table
#     # round the value of effect size into 2 decimal place
#     for a in range(len(es)):
#         es[a] = round(es[a], 2)
#
#     # round the value of statistical power from each nobs into 3 decimal place
#     for m in range(len(newArr)):
#         for n in range(len(newArr[m])):
#             newArr[m][n] = round(newArr[m][n], 3)
#
#
#     # prepare name colouns
#     for j in range(len(newArr)):
#         column = 'Power N: '+ str(nobsArr[j])
#         nameArr.append(column)
#
#     # prepare the values
#     for i in range(len(newArr)):
#         resultArr.append(newArr[i])
#
#     # Plotting them into a table
#     trace2 = go.Table(
#         header=dict(values=nameArr),
#         cells=dict(values=resultArr)
#     )
#
#
#     tableData = [trace2]
#
#     graphTable = json.dumps(tableData, cls=plotly.utils.PlotlyJSONEncoder)
#
#     return lineGraph, graphTable
