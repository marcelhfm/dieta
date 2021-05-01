import json
import pandas as pd
from pymysql import connections
from flaskr.dietDB import Database
import loadConfig
import sys


def connectDB():
    try:
        config = loadConfig.Config("diet.json")

        db = Database(config=config)
    
        return db
    except:
        for path in sys.path:
            print(path)
            
def execute_initDB():
    db = connectDB()
    
    db.initDB()
    
def test_insert_user():
    db = connectDB()
    user = json.loads('{"username": "Peter", "password": "supersecret123"}')

    db.insertUser(json_data=user)
    
def test_select_user(id):
    db = connectDB()
    user = db.selectUser(id)[0]['username']
    print(user)
    
def test_select_food(name):
    db = connectDB()
    food = db.selectFood(name)
    print(food)
    
def test_getUserId(username):
    db = connectDB()
    id = db.getUserID(username)#[0]['id']
    print(id)

def main():
    print("starting testing...")
    test_getUserId("Test")
    print("finished testing...")
    

if __name__ == "__main__":
    main()
