#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import pymysql
from time import gmtime, strftime
import re

# create logger
module_logger = logging.getLogger('diet.dietDB')

class Database():

    # Init database - drop and recreate table
    def initDB(self):
        try:
            self.cursor=self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`food`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not drop diet table for recreation! " +  ex.__class__)
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`food` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `user` varchar(50) DEFAULT NOT NULL"
                   "  `food` varchar(50) DEFAULT NOT NULL, "
                   "  `calories` decimal(14,8) DEFAULT NULL, "
                   "  `carbs` decimal(14,8) DEFAULT NULL, "
                   "  `protein` decimal(14,8) DEFAULT NULL, "
                   "  `fat` decimal(14,8) DEFAULT NULL, "
                   "  `refdate` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table diet! " + ex.__class__)
            return False

    # Initialize DB connection
    def __init__(self, config):
        self.logger = logging.getLogger('dieta.dietDB.Database')
        self.logger.debug("Logging is enabled in module " + __name__)

        dbhost = config.getItem("DBHOST")
        dbuser = config.getItem("DBUSER")
        dbpasswd = config.getItem("DBPASSWD")
        dbname = config.getItem("DBNAME")

        try:
            self.conn=pymysql.connect(host = dbhost,
                                        user = dbuser,
                                        password = dbpasswd,
                                        db = dbname,
                                        charset = 'utf8mb4',
                                        cursorclass = pymysql.cursors.DictCursor)
            self.cursor=self.conn.cursor()
            self.logger.debug("Connection to database established...")
        except Exception as ex:
            self.logger.critical("Could not establish database connection! " + ex.__class__)

    # Close DB connection
    def closeConnection(self):
        try:
            self.cursor.close()
        except Exception as ex:
            self.logger.critical("Could not close cursor! " + ex.__class__)

        try:
            self.conn.close()
        except Exception as ex:
            self.logger.critical("Could not close database connection! " + ex.__class__)
            return

        self.logger.debug("Database connection closed...")

    # Insert a new dataset (json record) into database
    # Return the last row id after insert completion
    def insertData(self, json_data):
        self.logger.debug("JSON data: " + json_data)
        if not "calories" in json_data:
            json_data["calories"]= "NULL"
            self.logger.error("Insert data: No sensor id given!")
        if not "carbs" in json_data:
            json_data["carbs"]= "NULL"
        if not "protein" in json_data:
            json_data["protein"]= "NULL"
        if not "fat" in json_data:
            json_data["fat"]= "NULL"

        sql= ("insert into food (user, food, calories, carbs, protein, fat, refdate)" + " values ('" +
            json_data["user"] + "'," +
            json_data["food"] + "," +
            str(json_data["calories"]) + "," +
            str(json_data["carbs"]) + ",'" +
            str(json_data["protein"]) + "','" +
            str(json_data["fat"]) + ")")

        re.sub(r'"NULL"', 'NULL', sql)
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor=self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database insert completed...")
        except Exception as ex:
            self.logger.critical("Could not insert data into database table: " + ex.__class__)
            return -1

        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + ex.__class__)
            return -1

        self.logger.info("Dataset successfully committed to database!")
        return self.cursor.lastrowid

    # Select a new dataset based on user and food and return json record
    def selectData(self, selectuser, selectfood):
        self.logger.debug("user: " + user + "; food: " + food)

        sql= ("select * from food where `user` like selectuser and `food` like selectfood")

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor=self.conn.cursor()
            self.cursor.execute(sql)

            result = [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]

            self.logger.debug("Database select completed...")
        except Exception as ex:
            self.logger.critical("Could not select data from database table: " + ex.__class__)
            return -1

        return result
