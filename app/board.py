# -*- coding: utf-8 -*-

from django.shortcuts import render

from app import consts
from app import mydb
from app.common import get_records_set_json, json_dumps
from app.auth import get_default_context

def board_theme_list():
    db = mydb.MyDB()
    rs = db.SqlQuery(db.sql('board_theme_list'))
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
        {'text': consts.NAV_CAPTION, 'link': '/'},
        {'text': 'Форум', 'link': '/board/', 'last': True}
    ]
    context['BREAD_CRUMBS'] = json_dumps(bread_crumbs)

    return render(
        request,
        'app/board/main.html',
        context
    )


def get_board_theme_comments(request, theme_id, page=1):
    context = get_default_context(request)
    db = mydb.MyDB()
    title = db.SqlQueryScalar(db.sql('board_theme_title'), {'id': theme_id})

    bread_crumbs = [{'text': consts.NAV_CAPTION, 'link': '/'}]
    bread_crumbs.append({'text': 'Форум', 'link': '/board/'})
    bread_crumbs.append({'text':  title, 'last': True})
    context['BREAD_CRUMBS'] = json_dumps(bread_crumbs)
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
