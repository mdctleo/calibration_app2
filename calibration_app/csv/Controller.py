from calibration_app.csv import bp
from flask import request
import csv
import json
import os
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError


@bp.route('/csv', methods=['POST'])
# @bp.route('/isotope/<name>', methods=['GET', 'PUT', 'DELETE'])
def counter():
    # if request.method == 'GET':
    #     return getIsotope(name)
    if request.method == 'POST':
        print(request.files)
        files = request.files.getlist('files')
        print(files)
        filesJson = []
        for file in files:
            filename = file.filename
            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            csvFile = file.read().decode()
            print(csvFile)

            # dialect = csv.Sniffer().sniff(csvFile)
            # print(csvFile)
            fieldnames = ("Protocol ID",
                          "Protocol name",
                          "Measurement date & time",
                          "Completion status",
                          "Run ID",
                          "Rack",
                          "Det",
                          "Pos",
                          "Time",
                          "Sample code",
                          "F-18 Counts",
                          "F-18 CPM",
                          "F-18 Error %",
                          "F-18 Info")
            reader = csv.DictReader(csvFile, fieldnames=fieldnames)
            data = []
            for row in reader:
                print(row)
                data.append(row)

            # jsonData = json.dumps(data)
            # print(jsonData)
            # data = json.loads(fileJson)
            # formattedJson = json.dumps(data, indent=4, sort_keys=True)
            # print(formattedJson)


        # repr(file)
        return "Got Here"