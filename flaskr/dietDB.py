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

        #target
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`target`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop target table for recreation! " + str(ex))
            return False

        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`target` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `refUserID` int(11) NOT NULL, "
                   "  `week` int DEFAULT NULL, "
                   "  `period` int DEFAULT NULL, "
                   "  `targetWeight` decimal(14, 8) DEFAULT NULL,"
                   "  `calories` decimal(14, 8) DEFAULT NULL, "
                   "  `protein` decimal(14, 8) DEFAULT NULL, "
                   "  `carbs` decimal(14, 8) DEFAULT NULL, "
                   "  `fats` decimal(14, 8) DEFAULT NULL, "
                   "  PRIMARY KEY (`id`), "
                   "  FOREIGN KEY (refUserID) REFERENCES user(id) "
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
                   "  `refUserID` int(11) NOT NULL, "
                   "  `refFoodID` int(11) NOT NULL, "
                   "  `currentWeight` decimal(14, 8) DEFAULT NULL,"
                   "  `amount` decimal(14, 8) DEFAULT NULL, "
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`), "
                   "  FOREIGN KEY (refUserID) REFERENCES user(id), "
                   "  FOREIGN KEY (refFoodID) REFERENCES food(id) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table weekly! " + str(ex))
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

        m = re.search('[^0-9a-zA-ZäöüßÄÖÜ%-]', json_data["username"], re.UNICODE)
        if not (isinstance(m, type(None))):
            self.logger.critical("%s contains illeagal characters which makes select statement tainted!" % json_data["username"])
            return json.loads('{"Result": "invalid search string: %s"}' % json_data["username"])
        
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
        else:
            if not isinstance(json_data["calories"], int):
                self.logger.error("calories is not numeric! : " + str(json_data["calories"]))
                return json.loads('{"Result": "calories is not numeric: %s"}' % json_data["calories"])
        if not "carbs" in json_data:
            json_data["carbs"]= "NULL"
        else:
            if not isinstance(json_data["carbs"], int):
                self.logger.error("carbs is not numeric! : " + str(json_data["carbs"]))
                return json.loads('{"Result": "carbs is not numeric: %s"}' % json_data["carbs"])
        if not "protein" in json_data:
            json_data["protein"]= "NULL"
        else:
            if not isinstance(json_data["protein"], int):
                self.logger.error("protein is not numeric! : " + str(json_data["protein"]))
                return json.loads('{"Result": "protein is not numeric: %s"}' % json_data["protein"])
        if not "fat" in json_data:
            json_data["fat"]= "NULL"
        else:
            if not isinstance(json_data["fat"], int):
                self.logger.error("fat is not numeric! : " + str(json_data["fat"]))
                return json.loads('{"Result": "fat is not numeric: %s"}' % json_data["fat"])
        
        sql= ("insert into food (food, calories, carbs, protein, fat)" + " values ('" +
            str(json_data["food"]) + "'," +
            str(json_data["calories"]) + "," +
            str(json_data["carbs"]) + "," +
            str(json_data["protein"]) + "," +
            str(json_data["fat"]) + ")")

        re.sub(r'"NULL"', 'NULL', sql, re.IGNORECASE)
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

    # Insert a new dataset (json record) into database
    # Return the last row id after insert completion
    def insertWeekly(self, userID, json_data):
        self.logger.debug("JSON data: " + json.dumps(json_data))
        if not "loss" in json_data:
            json_data["loss"]= "NULL"
            self.logger.error("Insert data: No loss given!")
        if not "deficit" in json_data:
            json_data["deficit"]= "NULL"
            self.logger.error("Insert data: No deficit given!")
        if not "protein" in json_data:
            json_data["protein"]= "NULL"
            self.logger.error("Insert data: No protein given!")
        if not "fat" in json_data:
            json_data["fat"]= "NULL"
            self.logger.error("Insert data: No fat given!")

        sql= ("insert into weekly (refUserID, loss, deficit, protein, fat)" + " values ('" +
            userID + "'," +
            json_data["calories"] + "," +
            json_data["carbs"] + "," +
            json_data["protein"] + "," +
            json_data["fat"] + ")")

        re.sub(r'"NULL"', 'NULL', sql, re.IGNORECASE)
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
        """Select all food records matching selectfood and return json record

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
    
    def selectUser(self, selectid):
        """Get user data of the specified user via id

        Args:
            selectid (String): Search string

        Returns:
            user json data
        """
        selectid = str(selectid)
        
        self.logger.debug("user: " + selectid)

        sql = ("SELECT * FROM user WHERE `id` = '" + selectid + "'")

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)

            result = self.cursor.fetchall()
            self.logger.debug("Database update completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
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

        m = re.search('[^0-9a-zA-ZäöüßÄÖÜ-]', selectuser)
        if not (isinstance(m, type(None))):
            self.logger.critical(
                "%s contains illeagal characters which makes select statement tainted!" % selectuser)
            return json.loads('{"Result": "invalid search string: %s"}' % selectuser)
        else:
            sql = ("select id from user where `username` like  '" + selectuser + "'")

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

    def updateUserWeight(self, userID, weight):
        """Update weight for the specified userID

        Args:
            userID (String): Search string
            weight (float): Value to be updated

        Returns:
            1 for success
        """
        self.logger.debug("user: " + userID + " weight: " + str(weight))

        
        if not isinstance(weight, int):
            self.logger.critical(
                "weight is not numeric:" + str(weight))
            return json.loads('{"Result": "invalid weight value: %s"}' % str(weight))
        
        sql = ("update `user` set `currentWeight` = %f where `id` = %s" % (weight, userID))  
        
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database update completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
            return -1

        return 1

    def updateMacroData(self, userID, json_data):
        """Update macro data for the specified user

        Args:
            userID (String): Search string
            json_data (dict): "calories":float, "protein":float, ...

        Returns:
            1 for success
        """
        self.logger.debug("user: " + userID + " data: " + str(json_data))

        sql = "update `user` set"
        for key in json_data:
            value = json_data[key]
            if isinstance(value, int):
                sql += " `%s` = %f," % (key, value)
            else:
                return json.loads('{"Result": "value not numeric: %s"}' % str(value))
        sql = sql[:-1] + " where `user` like %s" % userID     # remove last ",", then add where-clause

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database update completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
            return -1

        return 1
