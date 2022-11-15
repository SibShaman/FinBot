from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db.servce_db import mysql_connect
from handlers.main_handler import run_bot

app = Flask(__name__)


run_bot()


if __name__ == '__main__':
    app.run()
