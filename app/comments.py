# -*- coding: utf-8 -*-
from app import consts
from app import mydb
from app.user import get_avatar
from app.message import safe_msg_text
from app.message import message_write


def get_comments(params, request):
    id_parent = int(params['id'])
    page = params.get('page', 1)
    if page is None or page < 1:
        page = 1

    offset = (page - 1) * consts.COUNT_COMMENTS_PAGE

    db = mydb.MyDB()
    rs = db.SqlQuery(
        db.sql('comments_get'),
        {
            'id_parent': id_parent,
            'page_size': consts.COUNT_COMMENTS_PAGE,
            'offset': offset
        }
    )

    get_safe_msg_text(rs)

    for r in rs:
        r['avatar'] = get_avatar(r['avatar'])

    pages_count = get_msg_pages_count(id_parent)
    res = {
        'pages_count': pages_count,
        'comments': rs
    }
    return res


def get_msg_pages_count(id_parent):
    db = mydb.MyDB()
    comments_count = db.SqlQueryScalar(db.sql('comments_count'), {'id_parent': id_parent})
    pages_count = 0
    if comments_count % consts.COUNT_COMMENTS_PAGE != 0:
        pages_count = (
            ((comments_count - (comments_count % consts.COUNT_COMMENTS_PAGE))
             // consts.COUNT_COMMENTS_PAGE) + 1
        )
    else:
        pages_count = comments_count // consts.COUNT_COMMENTS_PAGE
    return pages_count


def get_safe_msg_text(rs):
    for r in rs:
        r['text'] = safe_msg_text(r['text'])


def new_comment(params, request):
    if params['parent_id'] is None:
        raise Exception('Не передан идентификатор объекта')
    id_parent = int(params['parent_id'])
    message_write(request, None, params['g-recaptcha-response'], id_parent, params['text'])
    return {'result': True}
