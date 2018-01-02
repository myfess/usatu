# -*- coding: utf-8 -*-
import json

from app import mydb
from app import consts
from app.common import json_dumps


def cache_check(method_name, params):
    db = mydb.MyDB()

    sql = '''
        SELECT value
        FROM cache
        WHERE
            method = @method@
            AND params = @params@
            AND (NOW() at time zone 'UTC' - date_time) < interval '{CACHE_INTERVAL}'
        ORDER BY id DESC
        LIMIT 1
    '''.format(
        CACHE_INTERVAL=consts.CACHE_INTERVAL
    )

    rs = db.SqlQuery(sql, {
        'method': method_name,
        'params': json_dumps(params)
    })
    if rs:
        return True, rs[0]['value']
    return False, None


def cache_add(method_name, params, result):
    """
        Добавление/обновления параметров вызова и результата в кэш
    """

    db = mydb.MyDB()
    sql = '''
        WITH
            t AS (
                INSERT
                INTO cache (method, params, value, date_time)
                VALUES (@method@, @params@, @value@, NOW() at time zone 'UTC')
                RETURNING id
            )

        DELETE
        FROM cache
        WHERE
            id != (SELECT t.id FROM t)
            AND method = @method@
            AND params = @params@
    '''

    db.SqlQuery(sql, {
        'value': result,
        'method': method_name,
        'params': json_dumps(params)
    }, True)
