from django.http import HttpResponse
from django.db import connections

from app import mydb
from app.common import json_dumps, get_id


def highload_import(request):
    sql = '''
        SELECT
            ID,
            UNIX_TIMESTAMP(post_date) utime,
            post_title,
            post_content
        FROM wp_posts
        WHERE post_status = 'publish'
        ORDER BY id
    '''

    sql_tmpl = '''
        INSERT
        INTO message (id, id_parent, title, time, text, author, category, allow, attach, ip)
        VALUES (@id@, @id_parent@, @title@, @time@, @text@, @author@, @category@, @allow@, @attach@, @ip@)
    '''

    sql_tmpl2 = '''
        insert into blog(id, message_id) values (@id@, @message_id@)
    '''

    db2 = mydb.MyDB('default2')
    rs = db2.SqlQuery(sql, {})

    db = mydb.MyDB()
    for r in rs:
        _id = get_id()

        db.SqlQuery(sql_tmpl2, {
            'id': r['ID'],
            'message_id': _id
        }, True)

        db.SqlQuery(sql_tmpl, {
            'id': _id,
            'id_parent': 0,
            'title': r['post_title'],
            'time': r['utime'],
            'text': r['post_content'],
            'author': 'my_fess',
            'category': None,
            'allow': 'yes',
            'attach': 'no',
            'ip': None
        }, True)


    res = json_dumps({'bom': 'bom'})
    return HttpResponse(res, content_type='application/json')


def board_import_users(request):
    rid = -100

    sql = '''
        SELECT
            id, name, password, email, avatar
        FROM ipbmembers
        WHERE id > @id@
        ORDER BY id
        LIMIT 1000
    '''

    sql_tmpl = '''
        INSERT
        INTO members (id, name, password, email, avatar)
        VALUES (@id@, @name@, @password@, @email@, @avatar@)
    '''

    db = mydb.MyDB()

    while True:
        #connections['default4'].close()
        db2 = mydb.MyDB('default4')
        rs = db2.SqlQuery(sql, {'id': rid})

        if not rs:
            return

        rid = rs[-1]['id']

        for r in rs:
            db.SqlQuery(sql_tmpl, {
                'id': r['id'],
                'name': r['name'],
                'password': r['password'],
                'email': r['email'],
                'avatar': (None if r['avatar'] == 'noavatar' else r['avatar'])
            }, True)

    res = json_dumps({'bom': 'bom'})
    return HttpResponse(res, content_type='application/json')


def convert_batch(db, table_name, columns, rid):
    connections['default2'].close()
    db2 = mydb.MyDB('default2')
    sql = '''
        SELECT *
        FROM {table_name}
        WHERE id > @id@
        ORDER BY id
        LIMIT 1000
    '''.format(table_name=table_name)
    rs = db2.SqlQuery(sql, {'id': rid})
    if not rs:
        return None, 0
    for r in rs:
        convert_row(db, table_name, columns, r)
    return rs[-1]['id'], len(rs)


def convert_table(table_name):
    db = mydb.MyDB()
    db2 = mydb.MyDB('default2')

    sql = '''
        SELECT *
        FROM {table_name}
        LIMIT 1
    '''.format(table_name=table_name)

    rs = db2.SqlQuery(sql, {})

    if not rs:
        return

    columns = list(rs[0].keys())

    if 'id' not in columns:
        sql = '''
            SELECT *
            FROM {table_name}
        '''.format(table_name=table_name)
        rs = db2.SqlQuery(sql, {})

        for r in rs:
            convert_row(db, table_name, columns, r)
        return

    rid = -10
    while True:
        rid, rs_len = convert_batch(db, table_name, columns, rid)
        if not rs_len:
            break


def convert_row(db, table_name, columns, r):
    cols = ', '.join(['"{}"'.format(c) for c in columns])
    values = ', '.join(['@{}@'.format(c) for c in columns])
    sql = '''
        INSERT
        INTO {table_name} ({columns})
        VALUES({values})
    '''.format(
        table_name=table_name,
        columns=cols,
        values=values
    )
    db.SqlQuery(sql, r, True)


def convert(request):
    tables = [
        # "board_theme",
        # "cache",
        # "chairs",
        # "chat_messages",
        # "comments_mod",
        # "cookie_id",
        # "files",
        # "files_subjects",
        # "files_types",
        # "foto",
        # "foto_statistics",
        ################ "id",
        # "images",
        # "images_folders",
        # "meet",
        # "meet_fotos",
        "members",
        # "message"
        # "struct_message",
        # "teachers",
        # "users",
        # "vote"
    ]

    for t in tables:
        convert_table(t)
    res = json_dumps({'bom': 'bom'})
    return HttpResponse(res, content_type='application/json')
