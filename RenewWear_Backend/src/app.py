from flask import Flask
from controller.post_controller import post_controller
from model.config import get_db_connection


app = Flask(__name__)

post_controller(app)

if __name__ == '__main__' :
    app.run(debug=True,port=8080)
