# -*- coding: utf-8 -*-

from django.db import connections


class MyDB:
    def __init__(self):
        self.cursor = connections['default'].cursor()

    def _SqlQuery(self, sql, no_result=False):
        try:
            if not sql:
                return []

            self.cursor.execute(sql)

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

        for key, value in params.items():
            if value is None:
                sql = sql.replace('@' + key + '@', 'NULL')
            elif isinstance(value, str):
                sql = sql.replace('@' + key + '@', "'" + myescape(value) + "'")
            elif isinstance(value, bool):
                v = 'TRUE' if value else 'FALSE'
                sql = sql.replace('@' + key + '@', v)
            else:
                sql = sql.replace('@' + key + '@', str(int(value)))

        return self._SqlQuery(sql, no_result)


def myescape(s):
    s = s.replace("`", "\\`")
    s = s.replace("'", "\\'")
    s = s.replace("\\", "\\\\")
    return s
