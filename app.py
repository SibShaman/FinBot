from flask import Flask
import handlers


app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

handlers.run_bot()

if __name__ == '__main__':
    app.run()
