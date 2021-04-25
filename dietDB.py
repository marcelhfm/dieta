#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import pymysql
from time import gmtime, strftime
import re

# create logger
module_logger = logging.getLogger('diet.dietDB')

class Database():

    def initDB(self):
        try:
            self.cursor=self.conn.cursor()
            sql = "DROP TABLE IF EXISTS `joule`.`food`"
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not drop weatherdata table for recreation! " +  ex.__class__)
            return False

        try:
            sql = ("CREATE TABLE IF NOT EXISTS `joule`.`food` ( "
                   "  `id` int(11) NOT NULL AUTO_INCREMENT, "
                   "  `sensor_id` varchar(50) DEFAULT NULL, "
                   "  `temperature` decimal(14,8) DEFAULT NULL, "
                   "  `humidity` decimal(14,8) DEFAULT NULL, "
                   "  `pressure` decimal(14,8) DEFAULT NULL, "
                   "  `date` datetime DEFAULT CURRENT_TIMESTAMP, "
                   "  `devicetype` varchar(50) DEFAULT NULL, "
                   "  `source` varchar(50) NOT NULL, "
                   "  `createdAt` datetime, "
                   "  `updatedAt` datetime, "
                   "  PRIMARY KEY (`id`) "
                   ") ENGINE=InnoDB  DEFAULT CHARSET=utf8")
            self.logger.debug("SQL=" + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.logger.critical("Could not create table weatherdata! " + ex.__class__)
            return False

    def __init__(self, config):
        self.logger = logging.getLogger('weatherApp.weatherDB.Database')
        self.logger.debug("Logging is enabled in module " + __name__)

        if (config.getItem("SIMULATE") == 1):
            dbhost = config.getItem("SIMULATE_DBHOST")
            dbuser = config.getItem("SIMULATE_DBUSER")
            dbpasswd = config.getItem("SIMULATE_DBPASSWD")
            dbname = config.getItem("SIMULATE_DBNAME")
        else:
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


    def insertData(self, json_data):
        self.logger.debug("JSON data: " + json_data)
        if not "sensor_id" in json_data:
            json_data["sensor_id"]= "unknown"
            self.logger.error("Insert data: No sensor id given!")
        if not "temperature" in json_data:
            json_data["temperature"]= "NULL"
        if not "humidity" in json_data or json_data["humidity"] == -99.0:
            json_data["humidity"]= "NULL"
        if not "pressure" in json_data or json_data["pressure"] == -99.0:
            json_data["pressure"]= "NULL"
        if not "iaq" in json_data or json_data["iaq"] == -99.0:
            json_data["iaq"]= "NULL"
        if not "devicetype" in json_data:
            json_data["devicetype"]= "NULL"
        if not "source" in json_data:
            json_data["source"]= "olimex"

        sql= ("insert into weatherdata (sensor_id, temperature, humidity, pressure, devicetype, source, refDate, secs, refSecs)" + " values ('" +
            json_data["sensor_id"] + "'," +
            str(json_data["temperature"]) + "," +
            str(json_data["humidity"]) + "," +
            str(json_data["pressure"]) + ",'" +
            str(json_data["devicetype"]) + "','" +
            str(json_data["source"]) + "','" +
            str(json_data["refDate"]) + "'," +
            str(json_data["secs"]) + "," +
            str(json_data["refSecs"]) + ")")

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
