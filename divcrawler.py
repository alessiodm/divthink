import json
import os

from crawler import get_terms

from flask import Flask
from flask import request
from flask import render_template
from flask import current_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/diverge', methods=['POST'])
def diverge():
    search_string = request.form['search_string']
    secret = request.form['secret']
    if secret != current_app.config['s3cret']:
      return json.dumps({ "error": "Wrong secret" })
    results = get_terms(search_string)
    return json.dumps(results)

if __name__ == '__main__':
    app.debug = True
    app.config['s3cret'] = os.getenv('SECRET', 's3cret')
    host = '0.0.0.0'
    port = int(os.getenv('PORT', '8000'))
    app.run(host, port)

