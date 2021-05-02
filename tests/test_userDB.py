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
    
def test_select_user(username):
    db = connectDB()
    user = db.selectUser(username)
    print(user)
    
def test_select_food(name):
    db = connectDB()
    food = db.selectFood(name)
    print(food)
    
def test_getUserID(id):
    db = connectDB()
    user = db.getUserID(id)
    print(user)
    return user
    
def test_test():
    pass
    
def test_insert_target():
    user_id = 6
    data = {
        "week": '1',
        "period": '1',
        "targetweight": '80',
        "calories": '1500',
        "protein": '20',
        "carbs": '30',
        "fats": '50'
    }
    
    db = connectDB()
    db.insertTargetData(userID=user_id, json_data=data)

def main():
    print("starting testing...")
    user_id = test_getUserID("testing123")
    
    print(type(user_id))
    user_id = user_id[0]['id']
    print(user_id)
    
    test_select_user(user_id)
    print("finished testing...")
    

if __name__ == "__main__":
    main()
