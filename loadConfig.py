#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Config():

    def __init__(self, file, debug=False):
        if debug:
            print("Loading config file: " + str(file))
        try:
            with open(file) as json_file:
                self.json_data = json.load(json_file)
            if debug == True:
                print("Config data = " + str(self.json_data))
                print("Config loaded...")
        except Exception as e:
            print("Cannot load config: " + str(e))

    def getItem(self, configItem):
        return self.json_data[configItem]