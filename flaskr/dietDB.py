#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import pymysql
from time import gmtime, strftime
import re
from werkzeug.security import generate_password_hash
# create logger
module_logger = logging.getLogger('diet.dietDB')

class Database():

    def initDB(self):
        """Init databases - drop and recreate tables
        """
        #userdb
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`user`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop user table for recreation! " + str(ex))
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`user` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `username` varchar(50) NOT NULL, "
                   "  `password` varchar(200) NOT NULL, "
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table user! " + str(ex))
            return False
        
        #food db
        try:
            self.cursor=self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`food`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not drop food table for recreation! " +  str(ex))
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`food` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `food` varchar(50) NOT NULL, "
                   "  `calories` decimal(14,8) DEFAULT NULL, "
                   "  `carbs` decimal(14,8) DEFAULT NULL, "
                   "  `protein` decimal(14,8) DEFAULT NULL, "
                   "  `fat` decimal(14,8) DEFAULT NULL, "
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table food! " + str(ex))
            return False
        
        #weekly
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`weekly`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop weekly table for recreation! " + str(ex))
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`weekly` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `loss` decimal(14, 8) DEFAULT NULL, "
                   "  `deficit` decimal(14, 8) DEFAULT NULL, "
                   "  `weight` decimal(14, 8) DEFAULT NULL,"
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table weekly! " + str(ex))
            return False
        
        #daily
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`daily`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`daily` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `deficit` decimal(14, 8) DEFAULT NULL, "
                   "  `calories` decimal(14, 8) DEFAULT NULL, "
                   "  `protein` decimal(14, 8) DEFAULT NULL, "
                   "  `fats` decimal(14, 8) DEFAULT NULL, "
                   "  `carbs` decimal(14, 8) DEFAULT NULL, "
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table daily! " + str(ex))
            return False
        
        #macro
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`macro`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop macro table for recreation! " + str(ex))
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`macro` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `calories` decimal(14, 8) DEFAULT NULL, "
                   "  `protein` decimal(14, 8) DEFAULT NULL, "
                   "  `carbs` decimal(14, 8) DEFAULT NULL, "
                   "  `fats` decimal(14, 8) DEFAULT NULL, "
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table macro! " + str(ex))
            return False


    # Initialize DB connection
    def __init__(self, config):
        self.logger = logging.getLogger('diet.dietDB')
        self.logger.debug("Logging is enabled in module " + __name__)
        self.logger.setLevel(logging.DEBUG)

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
            self.logger.critical("Could not establish database connection! " + str(ex))

    # Close DB connection
    def closeConnection(self):
        try:
            self.cursor.close()
        except Exception as ex:
            self.logger.critical("Could not close cursor! " + str(ex))

        try:
            self.conn.close()
        except Exception as ex:
            self.logger.critical("Could not close database connection! " + str(ex))
            return

        self.logger.debug("Database connection closed...")

    def insertUser(self, json_data):
        """Insert user into database

        Args:
            json_data (.json): json file containing username and password of a user
            
        """
        self.logger.debug("JSON data:" + json.dumps(json_data))
        
        password = generate_password_hash(json_data["password"])
            
        sql = ("insert into user (username, password)" + " values ('" +
               json_data["username"] + "', '" +
               password + "')")
        
        self.logger.debug("SQL" + sql)
        print("SQL" + sql)
        
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database insert completed...")
        except Exception as ex:
            self.logger.critical(
                "Could not insert data into database table: " + str(ex))
            return -1
        
        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return -1

        self.logger.info("Dataset successfully committed to database!")
        return self.cursor.lastrowid
        

    # Insert a new dataset (json record) into database
    # Return the last row id after insert completion
    def insertFood(self, json_data):
        self.logger.debug("JSON data: " + json.dumps(json_data))
        if not "calories" in json_data:
            json_data["calories"]= "NULL"
            self.logger.error("Insert data: No calories given!")
        if not "carbs" in json_data:
            json_data["carbs"]= "NULL"
        if not "protein" in json_data:
            json_data["protein"]= "NULL"
        if not "fat" in json_data:
            json_data["fat"]= "NULL"

        sql= ("insert into food (food, calories, carbs, protein, fat)" + " values ('" +
            json_data["food"] + "'," +
            str(json_data["calories"]) + "," +
            str(json_data["carbs"]) + "," +
            str(json_data["protein"]) + "," +
            str(json_data["fat"]) + ")")

        re.sub(r'"NULL"', 'NULL', sql)
        self.logger.debug("SQL=" + sql)
        print("SQL=" + sql)

        try:
            self.cursor=self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database insert completed...")
        except Exception as ex:
            self.logger.critical("Could not insert data into database table: " + str(ex))
            return -1

        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return -1

        self.logger.info("Dataset successfully committed to database!")
        return self.cursor.lastrowid


    def selectFood(self, selectfood):
        """Select a new dataset based on user and food and return json record

        Args:
            selectfood (String): Search string

        Returns:
            json: json record
        """
        self.logger.debug("food: " + selectfood)

        if (selectfood == "%"):
            sql = 'select * from food'
            self.logger.debug("SQL=" + sql)
        else:
            m = re.search('[^a-zA-ZäöüßÄÖÜ%]', selectfood, re.UNICODE)
            if not (isinstance(m, type(None))):
                self.logger.critical("%s contains illeagal characters which makes select statement tainted!" % selectfood)
                return json.loads('{"Result": "invalid search string: %s"}' % selectfood)
            
            sql= ("select * from food where `food` like '" + selectfood + "'")
        
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor=self.conn.cursor()
            self.cursor.execute(sql)
     
            result = self.cursor.fetchall()
            #result = [dict((self.cursor.description[i][0], value) \
            #   for i, value in enumerate(row)) for row in self.cursor.fetchall()]

            self.logger.debug("Database select completed...")
        except Exception as ex:
            self.logger.critical("Could not select data from database table: " + str(ex))
            return -1

        return result
    
    def selectUser(self, selectuser):
        """Select a new dataset based on user and return json record

        Args:
            selectuser (String): Search string

        Returns:
            json: json record
        """
        self.logger.debug("user: " + selectuser)

        if (selectuser == "%"):
            sql = ("select * from user")
        else:
            m = re.search('[^a-zäöüßA-ZÄÖÜ%-]', selectuser)
            if not (isinstance(m, type(None))):
                self.logger.critical(
                    "%s contains illeagal characters which makes select statement tainted!" % selectuser)
                return json.loads('{"Result": "invalid search string: %s"}' % selectuser)
            else:
                sql = ("select * from user where `username` like " + selectuser)

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)

            result = self.cursor.fetchall()
            #result = [dict((self.cursor.description[i][0], value) \
            #   for i, value in enumerate(row)) for row in self.cursor.fetchall()]

            self.logger.debug("Database select completed...")
        except Exception as ex:
            self.logger.critical(
                "Could not select data from database table: " + str(ex))
            return -1

        return result

    def getUserID(self, selectuser):
        """Get id of the specified user

        Args:
            selectuser (String): Search string

        Returns:
            user id
        """
        self.logger.debug("user: " + selectuser)

        m = re.search('[^a-zäöüßA-ZÄÖÜ-]', selectuser)
        if not (isinstance(m, type(None))):
            self.logger.critical(
                "%s contains illeagal characters which makes select statement tainted!" % selectuser)
            return json.loads('{"Result": "invalid search string: %s"}' % selectuser)
        else:
            sql = ("select id from user where `username` like " + selectuser)

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)

            result = self.cursor.fetchall()
            self.logger.debug("Database select completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not select data from database table: " + str(ex))
            return -1

        return result