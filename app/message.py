# -*- coding: utf-8 -*-

import json
import time
import urllib
import urllib.parse
import urllib.request

from django.shortcuts import render
from django.utils.html import escape

from app import mydb
from app import auth
from app import consts
from app.common import get_default_context, get_ID, get_client_ip
from app.mf_code import mf_code
from app.user import user_string


def safe_msg_text(t):
    t = t.replace('\n', '[br]')
    t = escape(t)
    return mf_code(t)


def get_message_preview(params, request):
    return {'preview': safe_msg_text(params['text'])}


def release_message(params, request):
    user = auth.MyUser(request)

    mid = int(params['id'])

    if not user.is_editor():
        raise Exception('Недостаточно прав чтобы удалить сообщение')

    sql = '''
        UPDATE message
        SET allow = 'yes'
        WHERE id = @id@
    '''
    db = mydb.MyDB()
    db.SqlQuery(sql, {'id': mid}, True)
    return {'result': True, 'message_id': mid}


def delete_message(params, request):
    user = auth.MyUser(request)

    mid = int(params['id'])

    if not user.is_editor():
        raise Exception('Недостаточно прав чтобы удалить сообщение')

    sql = '''
        DELETE FROM message WHERE id = @id@
    '''
    db = mydb.MyDB()
    db.SqlQuery(sql, {'id': mid}, True)
    return {'result': True, 'message_id': mid}


def write_message(params, request):
    message_write(
        request,
        params['id'],
        params.get('g-recaptcha-response'),
        params.get('id_parent'),
        params['text'],
        params['title'],
        params['attach'],
        params['board_theme']
    )
    return {'result': True}


def get_message(params, request):
    """
        Получение сообщения для формы редактирования сообщения
    """

    mid = int(params['id'])

    user = auth.MyUser(request)
    db = mydb.MyDB()

    if not user.is_editor():
        raise Exception('У вас нет прав изменять это сообщение.')

    sql = '''
        SELECT
            id,
            id_parent,
            title,
            text,
            (attach = 'yes') AS attach
        FROM message
        WHERE id = @id@
    '''

    rs = db.SqlQuery(sql, {'id': mid})
    if len(rs) != 1:
        raise Exception('Сообщение не найдено')

    m = rs[0]
    m['text'] = m['text'].replace('[br]', '\n')
    m['can_delete'] = user.is_editor()
    m['is_comment'] = m['id_parent'] is not None and m['id_parent'] != 0
    m['is_news'] = not m['is_comment']
    m['is_board_theme'] = False
    return m


def get_message_top_category(cid):
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

        SELECT "EN" AS en, "RU" AS ru
        FROM t
        ORDER BY level DESC
        LIMIT 1
    '''

    rs = db.SqlQuery(sql, {'id': cid})
    return {
        'en': rs[0]['en'],
        'ru': rs[0]['ru']
    }


def full_message(request, mid=None, page=1, gotocomment=None):
    """ Просмотр сообщения целиком с комментариями """

    db = mydb.MyDB()
    context = get_default_context(request)

    sql = '''
        SELECT *
        FROM message m
        WHERE m.id = @mid@
    '''

    rs = db.SqlQuery(sql, {'mid': int(mid)})

    if len(rs) != 1:
        return render(
            request,
            'app/static/unknow.html',
            context
        )

    cat = get_message_top_category(int(rs[0]['category']))
    context['msg'] = get_message_text(request, rs[0])
    context['msg']['en'] = cat['en']
    context['msg']['ru'] = cat['ru']
    context['msg']['url_pageless'] = 'news/{}'.format(mid)
    context['ADDITIONAL_PARAMS'] = '''
        'comments_page': {},
    '''.format(page)
    context['COMMENT_ID'] = gotocomment

    return render(
        request,
        'app/messages/full_message.html',
        context
    )


def message_write(
        request, message_id, captcha, id_parent, text, title='', attach=False, board_theme=False):
    db = mydb.MyDB()
    user = auth.MyUser(request)

    if message_id is None and not verify_captcha(request, captcha):
        raise Exception('Неверно введенная капча')

    if message_id is not None and not user.is_editor():
        raise Exception('Недостаточно прав чтобы редактировать сообщение')

    text = text.replace('\n', '[br]')
    text = text.replace('\r', '')
    attach_str = 'yes' if attach else 'no'

    if message_id:
        sql = '''
            UPDATE message
            SET
                text = @text@,
                title = @title@,
                attach = @attach@
            WHERE id = @id@
        '''

        db.SqlQuery(sql, {
            'id': message_id,
            'text': text,
            'title': title,
            'attach': attach_str
        }, True)

        if board_theme:
            sql = '''
                UPDATE board_theme
                SET title = @title@
                WHERE id = (
                    SELECT id_parent
                    FROM message
                    WHERE id = @id@)
            '''

            db.SqlQuery(sql, {
                'id': message_id,
                'title': title
            }, True)
    else:
        dt_msg = int(time.time())

        if board_theme:
            theme_id = get_ID()
            id_parent = theme_id
            sql = '''
                INSERT INTO board_theme (id, title, author, dt, dt_last_msg, ipb_id)
                VALUES (@id@, @title@, @author@, @dt@, @dt_last_msg@, @ipb_id@)
            '''

            db.SqlQuery(sql, {
                'id': theme_id,
                'title': title,
                'author': user.username,
                'dt': dt_msg,
                'dt_last_msg': dt_msg,
                'ipb_id': None
            }, True)

        sql = '''
            INSERT INTO message (
                "id", "id_parent", "title", "time", "text",
                "author", "category", "allow", "attach", "ip"
            )
            VALUES (
                @id@, @id_parent@, @title@, @time@, @text@,
                @author@, @category@, @allow@, @attach@, @ip@
            )
        '''

        mid = get_ID()
        db.SqlQuery(sql, {
            'id': mid,
            'id_parent': (0 if id_parent is None else int(id_parent)),
            'title': title,
            'time': dt_msg,
            'text': text,
            'author': user.username,
            'category': (consts.USATU_NEWS_CATEGORY if id_parent is None else None),
            'allow': ('yes' if user.is_editor() else 'no'),
            'attach': attach_str,
            'ip': get_client_ip(request)
        }, True)

        if id_parent:
            # Пробуем обновить дату последнего сообщения на форуме
            sql = '''
                UPDATE board_theme
                SET dt_last_msg = @dt_last_msg@
                WHERE id = @id@
            '''
            db.SqlQuery(sql, {
                'id': int(id_parent),
                'dt_last_msg': dt_msg
            }, True)

        send_notification_mail(mid)


def send_notification_mail(_id):
    db = mydb.MyDB()

    sql = '''
        SELECT
            m1.author AS new_author,
            m2.author AS old_author,
            m1.text AS new_text,
            m2.text AS old_text,
            m2.id AS old_id,
            m.email
        FROM message m1
        INNER JOIN message m2 ON (m2.id_parent != 0 AND m2.id = m1.id_parent)
        LEFT JOIN members m ON (m.name = m2.author)
        WHERE m1.id = @id@
    '''

    rs = db.SqlQuery(sql, {'id': _id})
    if len(rs) != 1:
        return
    m = rs[0]

    _email = m['email']
    if _email == -1:
        return

    return
    # url = get_url_comment(m['old_id'])
    # $tpl = new MyTpl("messages/mail.html");
    # $tpl->Set("{USER_LOGIN}", user_string($m['new_author']), false);
    # $tpl->Set("{OLD_MESSAGE}", mf_code($m['old_text']), false);
    # $tpl->Set("{NEW_MESSAGE}", mf_code($m['new_text']), false);
    # $tpl->Set("{URL}", $url['url']);

    # if _email != -1:
    #     _subject = "Ответ на ваш комментарий..."
        #subject = "=?utf-8?B?" + base64_encode(_subject) + "?="

        # header = (
        #     'MIME-Version: 1.0\r\n'
        #     'Content-Type: text/html; charset="utf-8"\r\n'
        #     'From: consts.NAV_CAPTION <notify@consts.DOMEN>\r\n'
        # )
        # Отправляем запрос на godaddy
        # r = mail(_email, subject, $tpl->GetText(), header)


def get_url_comment(comment_id):
    db = mydb.MyDB()

    p_id = get_main_parent_id(comment_id)
    if p_id == -1:
        return -1

    _time = db.SqlQueryScalar('SELECT "time" FROM message WHERE id = @id@', {'id': comment_id})
    news = db.SqlQuery('SELECT * FROM message WHERE id = @id@', {'id': p_id})
    photos = db.SqlQuery('SELECT * FROM foto WHERE id = @id@', {'id': p_id})
    teachers = db.SqlQuery('SELECT * FROM teachers WHERE id = @id@', {'id': p_id})

    sql = '''
        SELECT *
        FROM message
        WHERE
            id_parent = @p_id@
            AND time < @time@
    '''
    comments = db.SqlQuery(sql, {'p_id': p_id, 'time': _time})
    page = int(len(comments) // consts.COUNT_COMMENTS_PAGE) + 1

    r = {'type': '', 'url': ''}
    if news:
        r['type'] = 'news'
        r['url'] = 'news/{}/{}/gotocomment/{}/'.format(p_id, page, comment_id)
    elif teachers:
        r['type'] = 'teacher'
        r['url'] = 'teachers/{}/{}/gotocomment/{}/'.format(p_id, page, comment_id)

    if photos:
        u_id = photos[0]['user_id']
        sql = '''
            SELECT *
            FROM foto
            WHERE user_id = @user_id@
            ORDER BY time DESC
        '''
        user_photos = db.SqlQuery(sql, {'user_id': u_id})
        j = 0
        for p in user_photos:
            if p['id'] == p_id:
                break
            j += 1
        r['type'] = 'photo'
        r['url'] = 'photos/{}/{}/new/-1/all/1/{}/gotocomment/{}/'.format(
            u_id, (j + 1), page, comment_id)

    return r


def get_main_parent_id(comment_id):
    db = mydb.MyDB()

    c = db.SqlQuery('SELECT id_parent, id FROM message WHERE id = @id@', {'id': comment_id})

    if len(c) != 1:
        return -1

    p = db.SqlQuery('SELECT id FROM message WHERE id = @id@', {'id': c[0]['id_parent']})

    if len(p) == 1:
        return get_main_parent_id(p[0]['id'])
    elif not p:
        if c[0]['id_parent'] == 0:
            return c[0]['id']
        return c[0]['id_parent']
    return -1


def message_navigation_writer(request, _id='null'):
    return message_navigation(request, 'writer', _id)

def message_navigation_comment(request, _id='null'):
    return message_navigation(request, 'comment', _id)

def message_navigation_board_theme(request, _id='null'):
    return message_navigation(request, 'board_theme', _id)


def message_navigation(request, mode, _id='null'):
    """ Рендер расширенной формы: написать комментарий, новость, тему на форуме """

    context = get_default_context(request)

    message_id = 'null'
    parent_id = 'null'
    board_theme = 'false' # Если true - новое тема на форуме

    if mode == 'writer':
        message_id = _id
    elif mode == 'comment':
        parent_id = _id
    elif mode == 'board_theme':
        message_id = _id
        board_theme = 'true'

    context['MESSAGE_ID'] = message_id
    context['PARENT_ID'] = parent_id
    context['BOARD_THEME'] = board_theme

    return render(
        request,
        'app/messages/write_message.html',
        context
    )


def get_count_comments(_id):
    """ Определение количества комментариев у новости """

    db = mydb.MyDB()
    _count = 0
    level = 0
    ids = [str(_id)]
    while ids and level < 10:
        # Максимальная глубина комментариев - 10
        # TODO: вынести в настройки
        level += 1
        sql = '''
            SELECT id
            FROM message
            WHERE id_parent IN ({})
        '''.format(', '.join(ids))
        rs = db.SqlQuery(sql)
        ids = []
        for r in rs:
            ids.append(str(r['id']))
        _count += len(rs)
    return _count


def get_message_text(request, m, is_comment=False):
    """
        Построение ленты нвостей
        Построение новости когда её просматриваешь
    """

    user = auth.MyUser(request)

    _text = m['text'].replace('\n', '[br]')
    _text = escape(_text)
    _text = mf_code(_text)

    m['message_text'] = _text
    m['is_comment'] = is_comment
    if not is_comment:
        m['count_comment'] = get_count_comments(m['id'])
    m['message_author'] = user_string(m['author'])
    m['message_id'] = m['id'] if m.get('id') else ''
    m['message_time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(m['time']))
    m['message_category'] = get_main_EN_from_ID(m['category'])
    m['stick'] = m['attach'] == 'yes'

    return m


def verify_captcha(request, g_recaptcha_response):
    if not consts.CAPTCHA_ON:
        # Если выключена проверка капчи просто выходим
        return True

    # Verify captcha
    post_data = {
        'secret': consts.CAPTCHA_SECRET,
        'response': g_recaptcha_response,
        'remoteip': get_client_ip(request)
    }

    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req, data=data)
    res = response.read().decode('utf-8')
    recaptcha_response = json.loads(res)
    return recaptcha_response['success']


def get_main_EN_from_ID(ID):
    db = mydb.MyDB()

    try:
        ID = int(ID)

        sql = '''
            SELECT "EN", id_parent
            FROM struct_message
            WHERE struct_message.id = @id@
        '''

        rs = db.SqlQuery(sql, {'id': ID})
        if not rs:
            return 'ERROR'
        r = rs[0]
        if r['id_parent'] != 0:
            return get_main_EN_from_ID(r['id_parent'])
    except Exception:
        return 'Ошибка в категории'

    return r['EN']
