import json
from flaskr.dietDB import Database
import loadConfig

config = loadConfig.Config("diet.json")

db = Database(config=config)

user = json.loads('{"username": "test5", "password": "1a4"}')

db.insertUser(json_data=user)
