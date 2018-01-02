# -*- coding: utf-8 -*-
import json

from app import mydb
from app import consts
from app.common import json_dumps


def cache_check(method_name, params):
    db = mydb.MyDB()
    sql = db.sql('cache_check').format(
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
    db.SqlQuery(db.sql('cache_add'), {
        'value': result,
        'method': method_name,
        'params': json_dumps(params)
    }, True)
