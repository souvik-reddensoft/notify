import urllib.parse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    __instance = None

    def __init__(self):
        self.db_connection = None
        self.mongo_uri = os.getenv("MONGO_CONNECTION_TEST_URI") if os.getenv("FLASK_ENV") == "test" else os.getenv("MONGO_CONNECTION_URI")
        self.mongo_user = os.getenv("MONGO_TEST_USER") if os.getenv("FLASK_ENV") == "test" else os.getenv("MONGO_USER")
        self.mongo_password = os.getenv("MONGO_TEST_PASSWORD") if os.getenv("FLASK_ENV") == "test" else os.getenv("MONGO_PASSWORD")

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(MongoDB, cls).__new__(cls)
        return cls.__instance

    def connect(self):
        try:
            if not self.db_connection:
                username = urllib.parse.quote(self.mongo_user)
                password = urllib.parse.quote(self.mongo_password)
                self.db_connection = MongoClient(self.mongo_uri % (username, password))
                self.db_connection.list_databases()
        except Exception as ex:
            raise ConnectionError("MongoDB database connection failed") from ex

    def __call__(self):
        if not self.db_connection:
            raise ConnectionError("Database not conencted")
        return self.db_connection.get_default_database()

instance = MongoDB()