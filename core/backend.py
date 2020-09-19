#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file: backend.py
@time: 2020/9/17 0017 20:37
@desc:
'''
import json

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins

app = Flask(__name__)
# 输出中文
app.config['JSON_AS_ASCII'] = False

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test_backend:lyj123456@127.0.0.1:3306/test_backend'
db = SQLAlchemy(app)
# token 管理
app.config['JWT_SECRET_KEY'] = 'spaceants '  # Change this!
jwt = JWTManager(app)

jenkins = Jenkins(
    'http://39.98.176.213:8080/',
    username='taikong',
    password='1128e8a49a0996fa44032ff8144dad6700'
)



class User(db.Model):
    # 修正
    __tablename__ = "space_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class TestCase(db.Model):
    # 修正
    __tablename__ = "space_testcase"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<TestCase %r>' % self.name



class TestCaseApi(Resource):
    @jwt_required
    def get(self):

        r = []
        for t in TestCase.query.all():
            res = {}
            res['id'] = t.id
            res['name'] = t.name
            res['description'] = t.description
            res['data'] = t.data
            r.append(res)
        return r

    @jwt_required
    def post(self):
        t = TestCase(
            name=request.json['name'],
            description=request.json['description'],
            data=request.json['data']
        )
        db.session.add(t)
        db.session.commit()
        return {
            'msg':'ok'
        }

    # todo : 更新用例
    @jwt_required
    def put(self):
        pass

    # TODO : 删除用例
    @jwt_required
    def delete(self):
        pass

class LoginApi(Resource):
    def get(self):
        User.query.all()
        return {'hello': 'world'}

    def post(self):
        # TODO :查询数据库
        username=request.json.get('username',None)
        # TODO :通常密码不建议原文存储
        password = request.json.get('password',None)
        user = User.query.filter_by(username=username, password=password).first()
        # 查询到用户名不存在处理
        # done：生成返回结构体
        if user is None:

            return jsonify(
                errcode=1,
                errmsg='用户名或者密码错误'
            )
        else:
            return {
                'errcode': 0,
                'errmsg': 'ok',
                'username':username,
                'token': create_access_token(identity=user.username)
            }



    # todo: 注册
    def put(self):
        pass

    # todo:注销
    def delete(self):
        pass

class TaskApi(Resource):
    # todo: 查询所有的任务
    def get(self):
        pass

    def post(self):
        # todo: 用例获取
        testcases = request.json.get('testcases', None)
        # done: 调度jenkins
        jenkins['0920_testcase_demo'].invoke(
            securitytoken='1128e8a49a0996fa44032ff8144dad6700',
            build_params={
                'testcases': testcases
            })

        return {
            'errcode': 0,
            'errmsg': 'ok'
        }

        # todo: 结果交给其他接口异步处理


class ReportApi(Resource):
    def get(self):
        # 展示报告数据和曲线图

        pass

    def post(self):
        # todo: pull模式 主动从jenkins中拉取数据
        jenkins['testcase'].get_last_build().get_resultset()
        # todo: push模式 让jenkins node主动push到服务器
        # todo: 把测试报告数据与测试报告文件保存
        pass


api.add_resource(TestCaseApi, '/testcase')
api.add_resource(LoginApi, '/login')
api.add_resource(TaskApi, '/task')
# todo: 注册
# api.add_resource(RegistryApi, '/regist')


if __name__ == '__main__':
    app.run(debug=True)