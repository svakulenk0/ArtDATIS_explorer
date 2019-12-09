#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Dec 9, 2019
.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Simple Flask app for searching the ES index
based on https://medium.com/faun/building-a-real-time-elastic-search-engine-using-python-32e05bcb9140
'''

from flask import Flask
from search import search_blueprint
app = Flask(__name__)
app.register_blueprint(search_blueprint)

if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True, threaded=True)
