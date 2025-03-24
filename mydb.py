import mysql.connector
from mysql.connector import Error  
import os   
from dotenv import load_dotenv

load_dotenv()

dataBase = mysql.connector.connect(
    host= os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE IF NOT EXISTS bigbang")

print("Database created successfully")