# -*- coding: utf-8 -*-

from django.shortcuts import render

from app import mydb
from app import auth
from app.common import get_default_context
from app.message import get_message_text, get_url_comment


def news_mod(request):
    db = mydb.MyDB()
    context = get_default_context(request)
    user = auth.MyUser(request)

    if not user.is_editor():
        return render(
            request,
            'app/static/403.html',
            context
        )

    sql = db.sql('mod_news')
    rs = db.SqlQuery(sql)
    news = []
    for r in rs:
        m = get_message_text(request, r)
        if m['category']:
            m['category_path'] = get_path_ID(int(m['category']))
        else:
            m['category_path'] = '[Не выбран раздел]'
        news.append(m)
    context['news'] = news

    return render(
        request,
        'app/mod/news.html',
        context
    )


def teachers_mod(request):
    db = mydb.MyDB()
    context = get_default_context(request)
    user = auth.MyUser(request)

    if not user.is_editor():
        return render(
            request,
            'app/static/403.html',
            context
        )

    context['teachers'] = db.SqlQuery(db.sql('mod_teachers'))
    return render(
        request,
        'app/mod/teachers.html',
        context
    )


def get_path_ID(_id):
    db = mydb.MyDB()
    _list = db.SqlQueryScalar(db.sql('mod_path'), {'id': _id})
    return ' / '.join(_list)


def comments_mod(request):
    """ Модерирование комментариев """

    db = mydb.MyDB()
    context = get_default_context(request)
    user = auth.MyUser(request)

    if not user.is_editor():
        return render(
            request,
            'app/static/403.html',
            context
        )

    _sql = db.sql('mod_comments')

    sql = _sql.format(
        cols='count(*) cnt',
        orderby='')

    context['COUNT_COMMENTS'] = db.SqlQueryScalar(sql)

    sql = _sql.format(
        cols='*',
        orderby='ORDER BY m.time DESC LIMIT 30')

    rs = db.SqlQuery(sql)
    comments = []
    for r in rs:
        m = get_message_text(request, r, is_comment=True)
        m['parent'] = get_url_comment(r['id'])
        comments.append(m)
    context['comments'] = comments

    return render(
        request,
        'app/mod/comments.html',
        context
    )
