#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file: backend.py
@time: 2020/9/17 0017 20:37
@desc:
'''
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)