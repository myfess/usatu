# -*- coding: utf-8 -*-
import json

from django.shortcuts import render

from app import consts
from app import mydb
from app.common import get_default_context, get_records_set_json


def board_theme_list():
    db = mydb.MyDB()
    sql = '''
        SELECT
            *,
            (SELECT count(*) FROM message WHERE id_parent = bt.id) cnt
        FROM board_theme bt
        ORDER BY dt_last_msg DESC
        LIMIT 40
    '''

    rs = db.SqlQuery(sql)
    d = []
    for r in rs:
        d.append([r['id'], r['title'], r['dt_last_msg'], get_pages_count(r['cnt'])])

    s = [
        {'n': 'id', 't': 'Число целое'},
        {'n': 'caption', 't': 'Строка'},
        {'n': 'dt_last_msg', 't': 'Число целое'},
        {'n': 'pages', 't': 'Число целое'}
    ]

    return get_records_set_json(s, d)


def get_pages_count(cs):
    pages = 0
    if (cs % consts.COUNT_COMMENTS_PAGE) != 0:
        pages = ((cs - (cs % consts.COUNT_COMMENTS_PAGE)) // consts.COUNT_COMMENTS_PAGE) + 1
    else:
        pages = cs // consts.COUNT_COMMENTS_PAGE
    return pages


def get_board_theme(request):
    context = get_default_context(request)
    context['PAGE_TITLE'] = 'Форум - '

    bread_crumbs = [
        {'text': 'USATU.com', 'link': '/'},
        {'text': 'Форум', 'link': '/board/', 'last': True}
    ]
    context['BREAD_CRUMBS'] = json.dumps(bread_crumbs)

    return render(
        request,
        'app/board/main.html',
        context
    )


def get_board_theme_comments(request, theme_id, page=1):
    context = get_default_context(request)
    db = mydb.MyDB()

    sql = '''
        SELECT COALESCE(
            (
                SELECT title
                FROM board_theme
                WHERE id = @id@
            ),
            ''
        )
    '''

    title = db.SqlQueryScalar(sql, {'id': theme_id})

    bread_crumbs = [{'text': 'USATU.com', 'link': '/'}]
    bread_crumbs.append({'text': 'Форум', 'link': '/board/'})
    bread_crumbs.append({'text':  title, 'last': True})
    context['BREAD_CRUMBS'] = json.dumps(bread_crumbs)
    context['THEME_ID'] = theme_id
    context['THEME_TITLE'] = title
    context['ADDITIONAL_PARAMS'] = '''
        'comments_page': {},
    '''.format(page)

    return render(
        request,
        'app/board/theme.html',
        context
    )
