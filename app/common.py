# -*- coding: utf-8 -*-

""" Набор общих функций """

import json
import time
import os

from django.conf  import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail

from app import consts
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


def get_id():
    """ Получить новый глобальный id """

    db = mydb.MyDB()
    _id = db.SqlQueryScalar(db.sql('common_get_id'))
    return _id


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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


def json_dumps(d):
    return json.dumps(d, ensure_ascii=False)


def read_file(name):
    _root = getattr(settings, 'BASE_DIR', os.getcwd())
    path = os.path.join(_root, name)
    with open(path, 'r', encoding='utf-8') as myfile:
        data = myfile.read()
        return data
    return ''


def my_mail(subject, html_content, email):
    if not email or email == -1:
        return

    if not consts.PRODUCTION:
        return

    text_content = strip_tags(html_content)

    send_mail(
        subject,
        text_content,
        '"{}" <root@{}>'.format(consts.NAV_CAPTION, consts.DOMEN),
        [email],
        fail_silently=False,
        html_message=html_content
    )
