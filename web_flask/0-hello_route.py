#!/usr/bin/python3
"""A script that starts a Flask web application"""

from flask import Flask

"""create the flask application"""
app = Flask(__name__)

"""define route for homepage"""
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


"""Run the Flask application on 0.0.0.0:5000"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
