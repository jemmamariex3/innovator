# import the Flask class from the flask module
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sys
sys.path.append('../google/api')
from google.api.api_python import *
import mimetypes

mimetypes.add_type('text/javascript', '.js')

# create the application object
app = Flask(__name__)
CORS(app)    #CORS origin issue still persists.. Hmmm.

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

tasks = [
    {
        'id': 1,
        'title': u'Start Chat',
        'description': u'Start Chat Request',
        'done': False
    }

]

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('index.html') # render a template

@app.route('/startchat', methods=['GET'])
def start_chat():
    return jsonify({'tasks': tasks})

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)