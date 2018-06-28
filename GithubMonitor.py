#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Tuuu Nya<song@secbox.cn>

from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from models import Leakage

app = Flask(__name__)
api = Api(app)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


class LeakageList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, help="Which page with data")
        parser.add_argument('page_size', type=int, default=10, help="Which page count with data")
        parser.add_argument('status', type=int, help="data status")
        parser.add_argument('language', type=str, help="which type with data")
        args = parser.parse_args()

        db_leakages = Leakage.query

        if args.get('status'):
            db_leakages = db_leakages.filter(Leakage.status == args.get('status'))

        if args.get('language'):
            db_leakages = db_leakages.filter(Leakage.language == args.get('language'))

        db_leakages = db_leakages.order_by(-Leakage.add_time)\
            .paginate(page=args.get('page'), per_page=args.get('page_size'))
        leakages = {
            'count': db_leakages.total,
            'pages': db_leakages.pages,
            'current_page': db_leakages.page,
            'per_page': db_leakages.per_page,
            'items': [],
        }

        for i in db_leakages.items:
            leakages['items'].append(i.to_json())

        return leakages


api.add_resource(LeakageList, '/api/leakage')


if __name__ == '__main__':
    app.run()