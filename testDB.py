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

import dietDB

version = "1.0.1"

# create logger with 'spam_application'
logger = logging.getLogger('diet')
logger.setLevel(logging.DEBUG)

if sys.version_info < (3, 4):
    reload(sys)
    sys.setdefaultencoding('utf8')

localdir = os.path.dirname(sys.argv[0])
if (localdir != ''):
    os.chdir(localdir)

def main():
    config = loadConfig.Config("diet.json")
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


    dbConnect = dietDB.Database(config)
    dbConnect.initDB()
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
