#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file: test_jenkins.py
@time: 2020/9/20 0020 3:47
@desc:
'''
from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    jenkins = Jenkins(
        'http://39.98.176.213:8080/',
        username='taikong',
        password='1128e8a49a0996fa44032ff8144dad6700'
    )


    jenkins['testcase'].invoke(
        securitytoken='1128e8a49a0996fa44032ff8144dad6700',
        build_params={
            'testcases': '.'
        })

    print(jenkins['testcase'].get_last_completed_build().get_console())