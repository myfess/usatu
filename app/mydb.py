# -*- coding: utf-8 -*-

import os

from django.db import connections
from django.conf  import settings

from app import consts


class MyDB:
    def __init__(self, db_name='default'):
        self.cursor = connections[db_name].cursor()

    def _SqlQuery(self, sql, params, no_result=False):
        try:
            if not sql:
                return []

            self.cursor.execute(sql, params)

            if no_result:
                #self.cursor.commit()
                return None

            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            print('Ошибка выполнение запроса: {err}'.format(err=str(e)))
            raise e


    def SqlQueryScalar(self, sql, params=None, no_result=False):
        rs = self.SqlQuery(sql, params, no_result)
        if len(rs) != 1:
            raise Exception('SqlQueryScalar: Количество строк не может быть: {}'.format(len(rs)))
        keys = list(rs[0].keys())
        if len(keys) != 1:
            raise Exception(
                'SqlQueryScalar: Количество столбцов не может быть: {}'.format(len(keys))
            )
        return rs[0][keys[0]]


    def SqlQuery(self, sql, params=None, no_result=False):
        params = params if params else {}

        for key, _ in params.items():
            sql = sql.replace('@' + key + '@', '%(' + key + ')s')
        return self._SqlQuery(sql, params, no_result)


    def sql(self, name):
        _root = getattr(settings, 'BASE_DIR', os.getcwd())
        path = os.path.join(_root, consts.SQL_PATH, name + '.sql')
        with open(path, 'r') as myfile:
            data = myfile.read()
            return data
        return ''
