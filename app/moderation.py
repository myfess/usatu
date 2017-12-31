# -*- coding: utf-8 -*-

from django.shortcuts import render

from app import consts
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

    sql = '''
        SELECT *
        FROM message
        WHERE
            allow = 'no'
            AND id_parent = 0
        ORDER BY id DESC
        LIMIT 10
    '''
    rs = db.SqlQuery(sql)
    news = []
    for r in rs:
        m = get_message_text(request, r)
        m['category_path'] = get_path_ID(int(m['category']))
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

    sql = '''
        SELECT
            t.*,
            c.name AS chair
        FROM teachers t
        LEFT JOIN chairs c ON (c.id = t.id_chair)
        WHERE allow != 'yes'
        ORDER BY id DESC
        LIMIT 10
    '''
    context['teachers'] = db.SqlQuery(sql)
    return render(
        request,
        'app/mod/teachers.html',
        context
    )


def get_path_ID(_id):
    db = mydb.MyDB()
    sql = '''
        WITH RECURSIVE
            t AS (
                SELECT
                    *, 1 AS level
                FROM "struct_message"
                WHERE id = @id@

                UNION

                SELECT
                    sm.*, (t.level + 1) AS level
                FROM t
                INNER JOIN "struct_message" sm ON (sm.id = t.id_parent)
            )

        SELECT array_agg("RU" ORDER BY level DESC)
        FROM t
    '''
    _list = db.SqlQueryScalar(sql, {'id': _id})
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

    _sql = '''
        SELECT {cols}
        FROM message m
        WHERE
            NOT EXISTS (SELECT 1 FROM comments_mod c WHERE c.comment_id = m.id)
            AND m.id_parent != 0
            AND m.allow != 'yes'
            AND m.allow != 'forum'
        {orderby}
    '''

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
