#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Umstellung von DB Zugriff auf REST API, Ergänzung um BME280 Sensor

import loadConfig
import logging
from logging.handlers import RotatingFileHandler

import os
import sys
import requests
import json
import datetime
import platform
import getopt

from flask import Flask, render_template
from flask_socketio import SocketIO

from flaskr.dietDB import Database

version = "1.0.1"

# create logger with 'spam_application'
logger = logging.getLogger('diet')
logger.setLevel(logging.DEBUG)

localdir = os.path.dirname(sys.argv[0])
if (localdir != ''):
    os.chdir(localdir)
print("localdir={}".format(localdir))



def main():
    config = loadConfig.Config("../diet.json")
    logpath = config.getItem("LOGGERFILE")
    screenlogging = config.getItem("SCREENLOGGING")
    filelogging = config.getItem("FILELOGGING")
    progoptions = { 'logpath': logpath, 'logsize': 50000, 'logbackup': 10, 'screenlogging': screenlogging, 'filelogging': filelogging }

    if len(sys.argv) > 1 :
        try:
            options, remaining_args = getopt.getopt( sys.argv[1:],'hl:', \
                ["help", "logpath"] )
        except getopt.GetoptError as err:
            print(err)
            usage()
            exit(2)

        for opt,arg in options:
            if opt in ('-h', '--help'):
                usage()
                exit(0)
            elif opt in ('-l', '--logpath'):
                progoptions['logpath'] = arg
            elif opt in ('-s', '--logsize'):
                progoptions['logsize'] = arg
            elif opt in ('-b', '--logbackup'):
                progoptions['logbackup'] = arg
            elif opt in ('--screenlogging'):
                progoptions['screenlogging'] = arg.lower() or (progoptions['screenlogging']).lower()
            elif opt in ('--filelogging'):
                progoptions['filelogging'] = arg.lower() or (progoptions['filelogging']).lower()
            else:
                assert False, 'unhandled option'

    # create file handler which logs even debug messages
    #fh = logging.FileHandler(progoptions['logpath'])
    fh = RotatingFileHandler(progoptions['logpath'], mode='a', maxBytes=progoptions['logsize'], backupCount=progoptions['logbackup'])
    if (progoptions['screenlogging'] == 'debug'):
        fh.setLevel(logging.DEBUG)
        print("File: Log level set to <DEBUG>")
    elif (progoptions['screenlogging'] == 'info'):
        fh.setLevel(logging.INFO)
        print("File: Log level set to <INFO>")
    elif (progoptions['screenlogging'] == 'warn'):
        fh.setLevel(logging.WARN)
        print("File: Log level set to <WARN>")
    else:
        fh.setLevel(logging.ERROR)
        print("File: Log level set to <ERROR>")

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    if (progoptions['filelogging'] == 'debug'):
        ch.setLevel(logging.DEBUG)
        print("Screen: Log level set to <DEBUG>")
    elif (progoptions['filelogging'] == 'info'):
        ch.setLevel(logging.INFO)
        print("Screen: Log level set to <INFO>")
    elif (progoptions['filelogging'] == 'warn'):
        ch.setLevel(logging.WARN)
        print("Screen: Log level set to <WARN>")
    else:
        ch.setLevel(logging.ERROR)
        print("Screen: Log level set to <ERROR>")

    # create formatter and add it to the handlers
    formatterScreen = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatterFile   = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d : %(message)s')
    ch.setFormatter(formatterScreen)
    fh.setFormatter(formatterFile)
    # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.info("Logfile path is set to: " + progoptions['logpath'])
    logger.debug("Logging is enabled in Module: " + __name__)


    dbConnect = Database(config)
    if(False):
        dbConnect.initDB()
        testrecord = json.loads('{"food": "Birne", "calories": 10}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Ei", "calories": 100, "fat": 100}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Brie", "calories": 1000, "fat": 1000, "carbs": 1000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Apfel", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Weizenbrot", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Emmerbrot", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Camenbert", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Banane", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Ananas", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Aprikose", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Apfelmus", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Avocado", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Blaubeere", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Blutorange", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Brombeere", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Datteln", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Feigen", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)
        testrecord = json.loads('{"food": "Clementine", "calories": 10000, "fat": 10000, "carbs": 10000, "protein": 10000}')
        dbConnect.insertFood(testrecord)

        testrecord = json.loads('{"username": "Mario", "password": "23r4@~asoiu"}')
        dbConnect.insertUser(testrecord)
        testrecord = json.loads('{"username": "Mario", "password": "23r4@~asoiu"}')
        dbConnect.insertUser(testrecord)
        testrecord = json.loads('{"username": "Mario2", "password": "23r4@~asoiu"}')
        dbConnect.insertUser(testrecord)
        testrecord = json.loads('{"username": "Mario-3", "password": "23r4@~asoiu"}')
        dbConnect.insertUser(testrecord)
        testrecord = json.loads('{"username": "Johannes", "password": "23r4@~asoiu"}')
        dbConnect.insertUser(testrecord)


    print(dbConnect.selectFood('%1'))
    # change the JSON string into a JSON object
    #jsonObject = json.loads(dbConnect.selectFood('%'))
    jsonObject = dbConnect.selectFood('B%')

    if(False):
        # print the keys and values
        for obj in jsonObject:
            id = obj["id"]
            for key in obj:
                value = obj[key]
                if (key != "id"):
                    print("{:3}: {:8} = {}".format(id, key, value))

    if(False):
        # print json
        print("[")
        for obj in jsonObject:
            print("  {")
            for key in obj:
                value = obj[key]
                if (key == "food" or key == "refdate"):
                    print("    \"{}\":\"{}\"".format(key, value) + ",")
                else:
                    if (value == None):
                        print("    \"{}\":\"\"".format(key) + ",")
                    else:
                        print("    \"{}\":{}".format(key, value) + ",")
            print("  },")
        print("],")
        
    print("get userID for Mario")
    userID = dbConnect.getUserID('Mario')[0]
    print(userID)
    for key in userID:
        print("key:   " + key)
        print("value: " + str(userID[key]))
        userID = userID[key]

    print("get userID for Mario%")
    print(dbConnect.getUserID('Mario%'))
    
    print("update user weight")
    dbConnect.updateUserWeight(userID,81.7)
    
    print("get userID for Mario2")
    userID = dbConnect.getUserID('Mario2')[0]
    print(userID)
    for key in userID:
        print("key:   " + key)
        print("value: " + str(userID[key]))
        userID = userID[key]
    print("update user weight")
    dbConnect.updateUserWeight(userID,82.7)

    print("get userID for Gandalf")
    userID = dbConnect.getUserID('Gandalf')[0]
    print(userID)
    for key in userID:
        print("key:   " + key)
        print("value: " + str(userID[key]))
        userID = userID[key]
    print("update user weight")
    dbConnect.updateUserWeight(userID,83.7)

    print("update macro data (protein, fat, carb)")
    dbConnect.updateMacroData(userID,{"protein":124,"fat":45,"carb":987})

    print("get all data for user Mario from user table")
    print(dbConnect.selectUser(userID))

    dbConnect.closeConnection()




def usage():
        print("Script optional parameters:")
        print("  -h --help        print this help")
        print("  -l --logpath     define logfile path and name")
        print("                   Default: '/var/log/weatherapp/weatherApp.log'")
        print("  -s --logsize     define logfile size (for log rotation)")
        print("                   Default: 50000 bytes")
        print("  -b --logbackup   define number of logfile backups")
        print("                   Default: 10 log files")

if __name__ == '__main__':

    main()
