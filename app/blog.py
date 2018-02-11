# -*- coding: utf-8 -*-

from django.shortcuts import render

from app import mydb
from app.auth import get_default_context
from app.message import get_message_text


def blog_post(request, post_id, page=1, gotocomment=None):
    db = mydb.MyDB()
    context = get_default_context(request)

    mid = db.SqlQueryScalar(db.sql('blog_post'), {'id': post_id})
    rs = db.SqlQuery(db.sql('message_full'), {'mid': mid})

    if len(rs) != 1:
        return render(
            request,
            'app/static/unknow.html',
            context
        )

    context['msg'] = get_message_text(request, rs[0], is_comment=False, blog=True)
    context['msg']['en'] = 'blog'
    context['msg']['ru'] = 'блог'
    context['msg']['url_pageless'] = 'post{}'.format(post_id)
    context['LEFT_MENU'] = False
    context['ADDITIONAL_PARAMS'] = '''
        'comments_page': {},
    '''.format(page)
    context['COMMENT_ID'] = gotocomment
    context['NAV_CAPTION'] = 'HighLoad.org'
    context['HIGHLOAD'] = True

    return render(
        request,
        'app/highload/full_message.html',
        context
    )
