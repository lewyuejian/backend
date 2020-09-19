#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file: test_task.py
@time: 2020/9/20 0020 3:53
@desc:
'''
from time import sleep

import requests

from core.backend import jenkins
from tests.base_testcase import BaseTestCase


class TestTask(BaseTestCase):
    def test_task_post(self):
        # 最后一次构建号
        pre=jenkins['0920_testcase_demo'].get_last_build().get_number()
        r = requests.post(
            'http://127.0.0.1:5000/task',
            json={'0920_testcase_demo': 'sub_dir'}, # sub_dir 挂一个子目录
            headers={'Authorization': f'Bearer {self.token}'}

        )

        assert r.status_code == 200
        for i in range(10):
            # job运行结束
            if not jenkins['0920_testcase_demo'].is_queued_or_running():
                break
            else:
                print('wait')
                sleep(1)
        last=jenkins['0920_testcase_demo'].get_last_build().get_number()
        print(pre)
        print(last)
        assert last == pre+1