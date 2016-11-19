#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Takes a filename as a strin then returns a summarized version of the data"""


import csv
import json


GRADES = {
    'A': float(1.00),
    'B': float(0.90),
    'C': float(0.00),
    'D': float(0.70),
    'F': float(0.60),
    }


def get_score_summary(filename):
    """Takes an argument whose data will be represented

    Args:
        row(str): reperesents a file name whose data will
        be read and interpretted.
    """
    data = {}
    fhandler = open(filename, 'r')
    csv_f = csv.reader(fhandler)

    for row in csv_f:
        if row[10] not in ['P', '', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    newdata = {}
    for value in data.itervalues():
        if value[0] not in newdata.iterkeys():
            val1 = 1
            val2 = GRADES[value[1]]
        else:
            val1 = newdata[value[0]][0] + 1
            val2 = newdata[value[0]][1] + GRADES[value[1]]
        newdata[value[0]] = (val1, val2)
        newdata.update(newdata)

    finaldata = {}
    for key in newdata.iterkeys():
        val1 = newdata[key][0]
        val2 = newdata[key][1]/newdata[key][0]
        finaldata[key] = (val1, val2)
    return finaldata


def get_market_density(filename):
    """Takes one argument, a filename.

    Args:
        filename(str): filename.
    """
    fhandler = open(filename, 'r')
    alldata = json.load(fhandler)
    newdata = alldata['data']
    finaldata = {}
    fhandler.close()
    for data in newdata:
        data[8] = data[8].strip()
        if data[8] not in finaldata.iterkeys():
            val = 1
        else:
            val = finaldata[data[8]] + 1
        finaldata[data[8]] = val
        finaldata.update(finaldata)
    return finaldata


def correlate_data(file1='inspection_results.csv',
                   file2='green_markets.json',
                   file3='result.json'):
    """Takes 3 arguments

    Args:
        file1(str): restraunt scores data.
        json(str): green_market data
        result: output of the function.
    """
    data1 = get_score_summary(file1)
    data2 = get_market_density(file2)
    result = {}
    for key2 in data2.iterkeys():
        for key1 in data1.iterkeys():
            if key1 == str(key2).upper():
                val1 = data1[key1][1]
                val2 = float(data2[key2])/(data1[key1][0])
                result[key2] = (val1, val2)
                result[key2] = (val1, val2)
                result.update(result)
    jdata = json.dumps(result)
    fhandler = open(file3, 'w')
    fhandler.write(jdata)
    fhandler.close()
