#db 연결 
from flask import Flask, jsonify
import pymysql
import pymysql.cursors

app = Flask(__name__)



# MySQL database 연결 설정
def get_db_connection():

    MYSQL_HOST = 'database-1.c90i40424i5z.ap-northeast-2.rds.amazonaws.com'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = 'tjqjxlavmf2024'
    MYSQL_DB = 'serverdb'

    return pymysql.connect(host=MYSQL_HOST,
                           user=MYSQL_USER,
                           password=MYSQL_PASSWORD,
                           db=MYSQL_DB,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
