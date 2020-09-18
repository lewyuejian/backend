#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file: test_testcase.py
@time: 2020/9/19 0019 4:31
@desc:对应的测试用例
'''
import requests
import datetime



def test_add():
    r=requests.post(
        'http://127.0.0.1:5000/testcase',
        json={
            'name': f'name {str(datetime.datetime.now())}', # name 在这里不能重复，所以价格时间戳
            'description': 'd',
            'data': ''
        }
    )
    #断言
    assert r.status_code == 200
    assert r.json()['msg'] == 'ok'

