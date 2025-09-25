import os
import mysql.connector
from dotenv import load_dotenv

# Carga variables desde .env
load_dotenv()

class Db:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("MYSQL_DB"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            auth_plugin='mysql_native_password'
        )
