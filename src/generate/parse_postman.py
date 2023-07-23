#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/22 9:51
# @Author  : tx.lei
# @File    : parse_postman.py


import json

import requests
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import do

path = r"./Postman API.postman_collection.json"

with open(path, "r", encoding="utf-8") as f:
    postman_data = json.load(f)


def render_json(data):
    # 创建 Jinja2 环境
    env = Environment(loader=FileSystemLoader('.'), extensions=[do])

    # 加载模板文件
    template = env.get_template('template.py.j2')

    # 渲染模板并生成 Python 代码
    output = template.render(data)
    print(output)


def parse_json(items):
    for item in items:

        # 如果是分组，则向下遍历
        if 'item' in item:
            print("================================")
            print(f"group name: {item['name']}")
            parse_json(item['item'])

        # 如果是一个http接口，则处理该接口
        if 'request' in item:
            print(f"接口名称: {item['name']}")
            name = item['name']

            #
            req = item['request']

            # 获取url
            url = req['url']['raw']
            if str(url).__contains__("openapi"):
                url = "/openapi" + url.split('openapi')[1]

            # 获取请求方式
            method = req['method']

            # 获取并处理header
            headers = {}
            # 解析请求头
            if 'header' in req:
                headers = {h['key']: h['value'] for h in req['header']}

            # 处理入参
            args = []

            # 解析query参数
            params = dict()
            if 'query' in req['url']:
                for query in req['url']['query']:
                    params[query['key']] = query['value']


                    # 处理入参
                    arg = {}
                    arg['name'] = query['key']
                    if 'disabled' in query and query['disabled'] is True:
                        arg['default'] = query['value']
                    else:
                        arg['default'] = None
                    args.append(arg)


            # 解析请求正文
            body = None
            if 'body' in req and 'raw' in req['body']:
                # body = json.loads(req['body']['raw'])
                body = req['body']['raw']

            # 处理入参


            generate_data = {
                'function_name': name,
                'description': name,
                'args': args,
                "url": url,
                "method": method,
                "headers": json.dumps(headers),
            }

            if len(params) != 0:
                print(f"params:{params}")
                generate_data["params"] = json.dumps(params)

            if body is not None:
                generate_data["data"] = body

            print(f"generate_data:{generate_data}")

            render_json(generate_data)


parse_json(postman_data['item'])

# render_json()
