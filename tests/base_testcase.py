#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file: base_testcase.py
@time: 2020/9/20 0020 3:55
@desc:
'''
import requests


class BaseTestCase:
    def setup_class(self):
        username = 'taikong'
        password = '123456'
        r = requests.post(
            'http://127.0.0.1:5000/login',
            json={
                'username': username,
                'password': password
            }
        )
        #print(r.json())
        self.token = r.json()['token']
