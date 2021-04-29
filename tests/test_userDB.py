from flaskr.dietDB import Database
import loadConfig

config = loadConfig.Config("diet.json")

db = Database(config=config)

db.init_userDB()