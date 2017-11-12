# Running this file will start a local Flask Server

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sessions/create", methods=['POST'])
def create_session():
    #
    # use `request` local variable to access data
    return

def join_session():
    return

if __name__ == '__main__':
	app.run()