import json

from crawler import get_terms

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/diverge', methods=['POST'])
def diverge():
    search_string = request.form['search_string']
    secret = request.form['secret']
    #if secret != 'D1verg3nt!':
    #    return json.dumps({ "error": "Wrong secret" })
    results = get_terms(search_string)
    return json.dumps(results)

if __name__ == '__main__':
    app.debug = True
    app.run()

