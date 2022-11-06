from flask import Flask
from handlers.main_handler import run_bot

app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

run_bot()

if __name__ == '__main__':
    app.run()
