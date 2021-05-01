import json

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
    
def test_insert_user():
    db = connectDB()
    user = json.loads('{"username": "test5", "password": "1a4"}')

    db.insertUser(json_data=user)
    
def test_select_user():
    db = connectDB()
    user = db.selectUser("Mario")
    print(user)
    
def test_select_food():
    db = connectDB()
    food = db.selectFood("Birne")
    print(food)

def main():
    print("starting testing...")
    test_select_food()
    print("finished testing...")
    

if __name__ == "__main__":
    main()