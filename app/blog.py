# -*- coding: utf-8 -*-
import json

from django.shortcuts import render

from app import consts
from app import mydb
from app.common import get_records_set_json, json_dumps
from app.auth import get_default_context
from app.message import get_message_text


def blog_post(request, post_id, page=1, gotocomment=None):
    db = mydb.MyDB()
    context = get_default_context(request)

    sql = '''
        SELECT message_id
        FROM blog
        WHERE id = @id@
    '''

    mid = db.SqlQueryScalar(sql, {'id': post_id})

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
