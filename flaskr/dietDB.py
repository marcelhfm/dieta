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

################################################################################
    #
    # Initialize database
    # 
################################################################################
    def initDB(self):
        """Init databases - drop and recreate tables

        Args:
            none
            
        Returns:
            Success:    json string {"Success": 1}
            Error:      json string ("Error":"Error description")
        """
        #drop all tables first, set foreign_key_checks = 0 to ignore constraints by foreign keys

        self.logger.info("dropping all tables")
        try:
            self.cursor = self.conn.cursor()
            sql = "SET FOREIGN_KEY_CHECKS = 0"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "setting foreign_key_check failed: %s"}' % str(ex))
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`user`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "dropping table user failed: %s"}' % str(ex))  
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`food`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "dropping table food failed: %s"}' % str(ex)) 
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`daily`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "dropping table daily failed: %s"}' % str(ex)) 
        try:
            self.cursor = self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`target`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "dropping table target failed: %s"}' % str(ex)) 
        try:
            self.cursor = self.conn.cursor()
            sql = "SET FOREIGN_KEY_CHECKS = 1"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical(
                "Could not drop daily table for recreation! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "setting foreign_key_check failed: %s"}' % str(ex))

        #user
        self.logger.info("create table user")
        try:
            # id is incremented automatically
            # user and food is mandatory - must not be NULL
            # refdate is updated automatically with each insert or update
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`user` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `username` varchar(50) NOT NULL, "
                   "  `password` varchar(200) NOT NULL, "
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`), "
                   "  CONSTRAINT userconstraint UNIQUE (`username`)"
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table user! " + str(ex))
            self.logger.critical("sql: " + sql)
            return json.loads('{"Error": "creation of user table failed: %s"}' % str(ex))

        #food
        self.logger.info("create table food")
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
            return json.loads('{"Error": "creation of food table failed: %s"}' % str(ex))
        try:
            #insert "__weight__" as default food value for food reference in daily for currentWeight documentation
            sql = "insert into food (food) values ('__weight__')" 
            self.logger.debug("Insert default into food table: " + sql)
            self.cursor=self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database insert completed...")
        except Exception as ex:
            self.logger.critical("Could not insert data into database table: " + str(ex))
            return json.loads('{"Error": "insert of default value __weight__ into table food failed: %s"}' % str(ex))

        #daily
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
            return json.loads('{"Error": "creation of daily table failed: %s"}' % str(ex))    

        #target
        self.logger.info("creating table target")
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
                   "  `refdate` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  PRIMARY KEY (`id`), "
                   "  FOREIGN KEY (refUserID) REFERENCES user(id) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table user! " + str(ex))
            return json.loads('{"Error": "creation of target table failed: %s"}' % str(ex))
       
################################################################################
    #
    # Manage database connections
    # 
################################################################################
    # Initialize DB connection
    def __init__(self, config):
        """Initialize database class

        Args:
            config (json): contains values required for opening database connection
                           - DBHOST
                           - DBUSER
                           - DBPASSWD
                           - DBNAME

        Returns:
            Success:    json string ("Success":1)
            Error:      json string ("Error":"Error description")
        """
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
            return json.loads('{"Error": "Could not establish database connection! %s"}' % str(ex))
        
        self.logger.debug("Database connection established...")
        #return json.loads('{"Success":1}') 

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
            return json.loads('{"Error": "Could not close database connection! %s"}' % str(ex))

        self.logger.debug("Database connection closed...")
        return json.loads('{"Success":"Database connection closed"}') 

################################################################################
    #
    # Insert functions to insert a new dataset (row) into the database
    # 
################################################################################
    def insertUser(self, json_data):
        """Insert user into database

        Args:
            json_data containing:
            username (String):  Mandatory value - allowed chars: 0-9a-zA-ZäöüßÄÖÜ-
            password (String):  Mandatory value
            
        Returns:
            Success:    json string ("Success":row id)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("JSON data:" + json.dumps(json_data))
        
        password = generate_password_hash(json_data["password"])

        m = re.search('[^0-9a-zA-ZäöüßÄÖÜ-]', json_data["username"], re.UNICODE)
        if not (isinstance(m, type(None))):
            self.logger.critical("%s contains illeagal characters which makes select statement tainted!" % json_data["username"])
            return json.loads('{"Error": "invalid search string: %s"}' % json_data["username"])
        
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
            return json.loads('{"Error": "insert failed: %s"}' % str(ex))
        
        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return json.loads('{"Error": "commit failed: %s"}' % str(ex))

        self.logger.info("Dataset successfully committed to database!")
        
        return json.loads('{"Success":%s' % str(self.cursor.lastrowid))


    def insertFood(self, json_data):
        """Insert food record

        Args:
            json_data containing:
            food (String):      Mandatory value - allowed chars: 0-9a-zA-ZäöüßÄÖÜ-
            calories (float):   Default = NULL
            carbs (float):      Default = NULL
            protein (float):    Default = NULL
            fat (float):        Default = NULL
            refDate (datetime): Default = current date

        Returns:
            Success:    json string ("Success":row id)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("JSON data: " + json.dumps(json_data))
        # check food for allowed characters
        m = re.search('[^a-zA-ZäöüßÄÖÜ-]', json_data["food"], re.UNICODE)
        if not (isinstance(m, type(None))):
            self.logger.critical("%s contains illeagal characters which makes select statement tainted!" % json_data["food"])
            return json.loads('{"Error": "invalid string: %s"}' % json_data["food"])
        if not "calories" in json_data:
            json_data["calories"]= "NULL"
            self.logger.error("Insert data: No calories given!")
        else:
            # check if value is a number - int or float
            if not isinstance(json_data["calories"], (int,float)):
                self.logger.error("calories is not numeric! : " + str(json_data["calories"]))
                return json.loads('{"Error": "calories is not numeric: %s"}' % json_data["calories"])
        if not "carbs" in json_data:
            json_data["carbs"]= "NULL"
        else:
            # check if value is a number - int or float
            if not isinstance(json_data["carbs"], (int,float)):
                self.logger.error("carbs is not numeric! : " + str(json_data["carbs"]))
                return json.loads('{"Error": "carbs is not numeric: %s"}' % json_data["carbs"])
        if not "protein" in json_data:
            json_data["protein"]= "NULL"
        else:
            # check if value is a number - int or float
            if not isinstance(json_data["protein"], (int,float)):
                self.logger.error("protein is not numeric! : " + str(json_data["protein"]))
                return json.loads('{"Error": "protein is not numeric: %s"}' % json_data["protein"])
        if not "fat" in json_data:
            json_data["fat"]= "NULL"
        else:
            # check if value is a number - int or float
            if not isinstance(json_data["fat"], (int,float)):
                self.logger.error("fat is not numeric! : " + str(json_data["fat"]))
                return json.loads('{"Error": "fat is not numeric: %s"}' % json_data["fat"])
        
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
            return json.loads('{"Error": "insert failed: %s"}' % str(ex))

        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return json.loads('{"Error": "commit failed: %s"}' % str(ex))

        self.logger.info("Dataset successfully committed to database!")
        
        return json.loads('{"Success":%s' % str(self.cursor.lastrowid))

    
    def insertTargetData(self, userID, json_data):
        """Insert target  data for the specified user

        Args:
            userID (String):        Mandatory value - reference to user table
            json_data containing:
            week (int):             Default = NULL
            period (int):           Default = NULL
            targetWeight (float):   Default = NULL
            calories (float):       Default = NULL
            protein (float):        Default = NULL
            carbs (float):          Default = NULL
            fats (float):           Default = NULL

        Returns:
            Success:    json string ("Success":row id)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("user: " + str(userID) + " data: " + str(json_data))

        sql = "insert into `target` (refUserID, "
        for key in json_data:
            sql += " `%s`," % key
        sql = sql[:-1] + ") values (%s" % userID     # remove last ","
        for key in json_data:
            value = json_data[key]
            if key in ("week", "period", "targetWeight", "calories", "protein", "carbs", "fats"):
                if isinstance(value, (int, float)):
                    sql += " %s, " % value
                else:
                    sql += " '%s', " % value
            else:
                self.logger.error("unknown key: %s value: %s" % (key,value))
                return json.loads('{"Error":"unknown key: %s value: %s" % (key,value)}')
        sql = sql[:-1] + ") "     # remove last ",", then add where-clause

        re.sub(r'"NULL"', 'NULL', sql, re.IGNORECASE)
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database update completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
            return json.loads('{"Error": "update failed: %s"}' % str(ex))

        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return json.loads('{"Error": "commit failed: %s"}' % str(ex))

        return json.loads('{"Success":%s' % str(self.cursor.lastrowid))

    def insertDailyData(self, userID, foodID, json_data):
        """Insert daily data for the specified user and food

        Args:
            userID (String):        Mandatory value - reference to user table
            foodID (String):        Mandatory value - reference to food table
            json_data containing:
            amount (int):             Default = NULL
            refDate (datetime):           Default = NULL
            
            NOT ALLOWED:
            currentWeight (float):  This has to be inserte via insertUserWeight function
                                    as the weight is associated with the special food 
                                    reference ID of "__weight__"

        Returns:
            Success:    json string ("Success":row id)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("user: " + str(userID) + " food: " + str(foodID) + " data: " + str(json_data))

        sql = "insert into `daily` (refUserID, refFoodID, "
        for key in json_data:
            sql += " `%s`," % key
        sql = sql[:-1] + ") values (%s" % userID     # remove last ","
        for key in json_data:
            value = json_data[key]
            if key == "currentWeight":
                self.logger.error("To insert currentWeight via insertDaily function is not allowed!")
                return json.loads('{"Error":"To insert currentWeight via insertDaily function is not allowed!"}')
            if key in ("amount", "refdate"):
                if isinstance(value, (int, float)):
                    sql += " %s, " % value
                else:
                    sql += " '%s', " % value
            else:
                self.logger.error("unknown key: %s value: %s" % (key,value))
                return json.loads('{"Error":"unknown key: %s value: %s" % (key,value)}')
        sql = sql[:-1] + ") "     # remove last ",", then add where-clause

        re.sub(r'"NULL"', 'NULL', sql, re.IGNORECASE)
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database update completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
            return json.loads('{"Error": "update failed: %s"}' % str(ex))

        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return json.loads('{"Error": "commit failed: %s"}' % str(ex))

        return json.loads('{"Success":%s' % str(self.cursor.lastrowid))

    def insertUserWeight(self, userID, weight):
        """Insert user weight for the specified userID

        Args:
            userID (String): Search string
            weight (float): Value to be updated

        Returns:
            Success:    json string ("Success":row id)
            Error:      json string ("Error":"Error description")
       """

        print(weight)
        print(userID)
        self.logger.debug("user: %s weight: %s" % (userID, weight))

        
        if not isinstance(weight, float):
            self.logger.critical(
                "weight is not numeric:" + str(weight))
            return json.loads('{"Error": "invalid weight value: %s"}' % str(weight))
        
        #Current weight record is always linked to the food reference with food name "__weight__"
        foodID = self.getFoodID('__weight__')[0]
        for key in foodID:
            print("key:   " + key)
            print("value: " + str(foodID[key]))
            foodID = foodID[key]

        sql = ("insert into `daily` (`refUserID`, `refFoodID`, `currentWeight`) values (%s, %s, %s)" % (userID, foodID, weight))  
        
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database update completed...")
        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
            return json.loads('{"Error": "update failed: %s"}' % str(ex))

        try:
            self.conn.commit()
            self.logger.debug("Database insert committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last insert: " + str(ex))
            return json.loads('{"Error": "commit failed: %s"}' % str(ex))

        return json.loads('{"Success":%s' % str(self.cursor.lastrowid))

################################################################################
    #
    # Select functions to extract datasets (rows) from the database
    # 
################################################################################

    def selectFood(self, selectfood):
        """Select all food records matching selectfood and return json record

        Args:
            selectfood (String): Search string

        Returns:
            Success:    json records (one or more)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("food: " + selectfood)

        if (selectfood == "%"):
            sql = 'select * from food'
            self.logger.debug("SQL=" + sql)
        else:
            m = re.search('[^a-zA-ZäöüßÄÖÜ%]', selectfood, re.UNICODE)
            if not (isinstance(m, type(None))):
                self.logger.critical("%s contains illeagal characters which makes select statement tainted!" % selectfood)
                return json.loads('{"Error": "invalid search string: %s"}' % selectfood)
            
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
            return json.loads('{"Error": "select failed: %s"}' % str(ex))

        return result
    
################################################################################
    #
    # Select functions to extract one dataset (row) from the database
    # 
################################################################################

    def getUserID(self, selectuser):
        """Get id of the specified user

        Args:
            selectuser (String): Search string

        Returns:
            Success:    json records (one)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("user: " + selectuser)

        m = re.search('[^0-9a-zA-ZäöüßÄÖÜ-]', selectuser)
        if not (isinstance(m, type(None))):
            self.logger.critical(
                "%s contains illeagal characters which makes select statement tainted!" % selectuser)
            return json.loads('{"Error": "invalid search string: %s"}' % selectuser)
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
            self.logger.critical(
                "sql: " + sql)
            return json.loads('{"Error": "select failed: %s"}' % str(ex))

        if (result.len() > 1):
            self.logger.critical("More than one datarow is returned!")
            return json.loads('{"Error": "more than one dataset returned: %s"}' % json.dumps(result))

        return result

    def getFoodID(self, selectfood):
        """Get id of the specified food

        Args:
            selectfood (String): Search string

        Returns:
            Success:    json records (one)
            Error:      json string ("Error":"Error description")
        """
        self.logger.debug("Food: " + selectfood)

        m = re.search('[^0-9a-zA-ZäöüßÄÖÜ_-]', selectfood)
        if not (isinstance(m, type(None))):
            self.logger.critical(
                "%s contains illeagal characters which makes select statement tainted!" % selectfood)
            return json.loads('{"Error": "invalid search string: %s"}' % selectfood)
        else:
            sql = ("select id from food where `food` like '%s'" % selectfood)

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)

            result = self.cursor.fetchall()
            self.logger.debug("Database select completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not select data from database table: " + str(ex))
            self.logger.critical(
                "sql: " + sql)
            return json.loads('{"Error": "select failed: %s"}' % str(ex))
        
        if (result.len() > 1):
            self.logger.critical("More than one datarow is returned!")
            return json.loads('{"Error": "more than one dataset returned: %s"}' % json.dumps(result))

        return result

    def selectUser(self, selectid):
        """Get user data of the specified user via id

        Args:
            selectid (String): Search string

        Returns:
            Success:    json records (one)
            Error:      json string ("Error":"Error description")
        """
        selectid = str(selectid)
        
        self.logger.debug("user: " + str(selectid))

        sql = ("SELECT * FROM user WHERE `id` = '" + str(selectid) + "'")

        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)

            result = self.cursor.fetchall()
            self.logger.debug("Database select completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not select data in database table: " + str(ex))
            return json.loads('{"Error": "select failed: %s"}' % str(ex))

        return result

################################################################################
    #
    # Update functions to update one dataset (row) in the database
    # 
################################################################################
    def updateUserWeight(self, userID, weight, date):
        """Update weight for the specified userID

        Args:
            userID (String):    Search value
            weight (float):     Value to be updated
            date (datetime):    Search value

        Returns:
            Success:    json string {"Success": 1}
            Error:      json string ("Error":"Error description")
        """

        print(weight)
        print(userID)
        self.logger.debug("user: %s weight: %s" % (userID, weight))

        
        if not isinstance(weight, float):
            self.logger.critical(
                "weight is not numeric:" + str(weight))
            return json.loads('{"Error": "invalid weight value: %s"}' % str(weight))
        
        #Current weight record is always linked to the food reference with food name "__weight__"
        foodID = self.getFoodID('__weight__')[0]
        for key in foodID:
            print("key:   " + key)
            print("value: " + str(foodID[key]))
            foodID = foodID[key]

        sql = ("insert into `daily` (`refUserID`, `refFoodID`, `currentWeight`) values (%s, %s, %s)" % (userID, foodID, weight))  
        
        self.logger.debug("SQL=" + sql)

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.logger.debug("Database update completed...")

        except Exception as ex:
            self.logger.critical(
                "Could not update data in database table: " + str(ex))
            return json.loads('{"Error": "update failed: %s"}' % str(ex))

        try:
            self.conn.commit()
            self.logger.debug("Database update committed...")
        except Exception as ex:
            self.logger.critical("Could not commit last update: " + str(ex))
            return json.loads('{"Error": "commit failed: %s"}' % str(ex))

        return json.loads('{"Success": 1}')

