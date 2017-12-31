# -*- coding: utf-8 -*-

""" Набор общих функций """

import time

from django.utils.safestring import mark_safe

from app import consts
from app import auth
from app import mydb

def get_latin_table():
    return {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'jo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'eh', 'ю': 'ju', 'я': 'ja',

        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'JO',
        'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'KH', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '',
        'Ы': 'Y', 'Ь': '', 'Э': 'EH', 'Ю': 'JU', 'Я': 'JA'
    }


def get_default_context(request):
    user = auth.MyUser(request)

    context = {
        'ADS': consts.ADS,
        'COUNTERS': consts.COUNTERS,
        'JIVOSITE': consts.JIVOSITE,
        'REFORMAL': consts.REFORMAL,
        'SAPE': consts.SAPE,
        'TYPESCRIPT': consts.TYPESCRIPT,
        'ES5': consts.ES5,
        'USATU_PATH': consts.USATU_PATH,
        'PRODUCTION_STR': 'true' if consts.PRODUCTION else 'false',
        'ADDITIONAL_PARAMS': '',
        'unentered_user': not user.is_registered(),
        'is_editor': user.is_editor(),
        'IS_EDITOR_STR': 'true' if user.is_editor() else 'false',
        'CFG_CAPTCHA_ON_STR': 'true' if consts.CAPTCHA_ON else 'false',
        'CAPTCHA_PUBLIC': consts.CAPTCHA_PUBLIC,
        'USER_LOGIN': user.username,
        'AVATAR': mark_safe("'{}'".format(user.avatar)) if user.avatar else 'null',
        'USER_ID': user.user_id,
        'COMMENT_ID': None
    }
    return context


def get_ID():
    """ Получить новый глобальный id """
    db = mydb.MyDB()
    sql = '''
        INSERT INTO "id"
        SELECT coalesce(MAX("id"."id") + 1, 1) FROM "id"
        RETURNING "id"
    '''
    _id = db.SqlQueryScalar(sql)
    return _id


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def myescape(s):
    s = s.replace("`", "\\`")
    s = s.replace("'", "\\'")
    s = s.replace("\\", "\\\\")
    return s


def get_records_set_json(s, d):
    res = {
        'jsonrpc': '2.0',
        'id': 1,
        'protocol': 4,
        'result': {
            's': s,
            'f': 0,
            'd': d,
            '_type': 'recordset',
            'n': False
        }
    }
    return res


def json_to_record(rec):
    r = {}
    if rec is None:
        return r
    for i in range(len(rec['s'])):
        r[rec['s'][i]['n']] = rec['d'][i]
    return r


def epoch_to_date_str(epoch):
    return time.strftime('%Y-%m-%d', time.localtime(epoch))