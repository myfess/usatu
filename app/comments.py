# -*- coding: utf-8 -*-
from app import consts
from app import mydb
from app.user import get_avatar
from app.message import safe_msg_text
from app.message import message_write


def get_comments(params):
    id_parent = int(params['id'])
    page = params.get('page', 1)
    if page is None or page < 1:
        page = 1

    offset = (page - 1) * consts.COUNT_COMMENTS_PAGE

    sql = '''
        SELECT
            message.*,
            m.avatar,
            0 AS level
        FROM message
        LEFT JOIN members m ON (m.name = message.author)
        WHERE id_parent = @id_parent@
        ORDER BY time
        LIMIT @page_size@
        OFFSET @offset@
    '''

    db = mydb.MyDB()
    rs = db.SqlQuery(sql, {
        'id_parent': id_parent,
        'page_size': consts.COUNT_COMMENTS_PAGE,
        'offset': offset
    })

    level = 0
    ids = get_msg_ids(rs)
    while ids and level < 10:
        # Максимальная глубина комментариев - 10
        # TODO: вынести в настройки
        level += 1
        ids_str = ', '.join(ids)
        sql = '''
            SELECT
                message.*,
                m.avatar,
                @level@ AS level
            FROM message
            LEFT JOIN members m ON (m.name = message.author)
            WHERE id_parent IN ({ids})
            ORDER BY time
        '''.format(ids=ids_str)

        rs_childs = db.SqlQuery(sql, {'level': level})
        ids = get_msg_ids(rs_childs)
        add_msg_children(rs, rs_childs)

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
    sql = '''
        SELECT count(*)
        FROM message
        WHERE id_parent = @id_parent@
    '''
    db = mydb.MyDB()
    comments_count = db.SqlQueryScalar(sql, {'id_parent': id_parent})
    pages_count = 0
    if comments_count % consts.COUNT_COMMENTS_PAGE != 0:
        pages_count = (
            ((comments_count - (comments_count % consts.COUNT_COMMENTS_PAGE))
             // consts.COUNT_COMMENTS_PAGE) + 1
        )
    else:
        pages_count = comments_count // consts.COUNT_COMMENTS_PAGE
    return pages_count


def add_msg_children(rs, rs_childs):
    """ Распределяем детей по родителям """

    for c in rs_childs:
        for i in range(len(rs) + 1):
            if (rs[i]['id'] == c['id_parent']
                    and (i == len(rs) - 1 or rs[i + 1]['id'] != c['id_parent'])):
                rs.insert(i + 1, c)
                break


def get_msg_ids(rs):
    return [str(r['id']) for r in rs]


def get_safe_msg_text(rs):
    for r in rs:
        r['text'] = safe_msg_text(r['text'])


def new_comment(params, request):
    if params['parent_id'] is None:
        raise Exception('Не передан идентификатор объекта')
    id_parent = int(params['parent_id'])
    message_write(request, None, params['g-recaptcha-response'], id_parent, params['text'])
    return {'result': True}
