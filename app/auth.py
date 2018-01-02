# -*- coding: utf-8 -*-
import time
import hashlib
import random

from app import consts
from app import mydb
from app.user import get_avatar, get_user_by


def sign_in(params, request):
    login = params['login']
    password = params['password']
    res = auth_sign_in(login, password)
    result = {
        'token': res['token']
    }
    if res['token'] is None:
        result['auth_msg'] = res['msg']
    return result


def sign_out(params, request):
    sid = request.COOKIES.get('usatu_auth', '')

    res = auth_sign_out(sid)
    if res:
        return {'result': True}
    else:
        raise Exception('Не удалось разлогиниться')


def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def get_rand_string(_id=0):
    _seed = int(time.time()) ^ int(_id)
    random.seed(_seed)
    digi = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
        'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
        'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z'
    ]
    res = ''
    n = len(digi)

    for _ in range(50):
        res += digi[random.randint(0, n - 1)]
    return res


def auth(auth_login, set_cookie=True):
    db = mydb.MyDB()

    sid = md5(get_rand_string())
    if set_cookie:
        # TODO: нет такой функции
        # SetCookie('usatu_auth', cookie_ID, time() + TIME_AUTH);
        pass
    sql = '''
        INSERT INTO cookie_id
        VALUES(@cookie_ID@, @auth_login@)
    '''
    db.SqlQuery(sql, {'cookie_ID': sid, 'auth_login': auth_login}, True)
    return sid


def get_permissions(login):
    db = mydb.MyDB()

    sql = '''
        SELECT permission
        FROM users
        WHERE login = @login@
    '''
    ps = db.SqlQuery(sql, {'login': login})

    if len(ps) != 1:
        return consts.USER_PERMISSION
    return ps[0]['permission']


def auth_sign_out(sid):
    db = mydb.MyDB()
    sql = '''
        DELETE
        FROM cookie_id
        WHERE cookie_id.id = @cookie_id@
    '''
    db.SqlQuery(sql, {'cookie_id': sid})
    #SetCookie('usatu_auth', 0, time() - 1000000);
    return True


def auth_sign_in(login, password):
    if login == '':
        return {'token': None, 'msg': 'Недопустимый логин'}

    user = get_user_by(None, login)
    if user['id'] == -1:
        return {'token': None, 'msg': 'Нет пользователя с таким логином'}

    password = md5(password)
    if password != user['password']:
        return {'token': None, 'msg': 'Неверный пароль'}

    token = auth(login, False)
    return {'token': token}


class MyUser:
    username = consts.GUEST
    permission = consts.GUEST_PERMISSION
    user_id = consts.GUEST_ID
    avatar = None

    def __init__(self, request):
        sql = '''
            SELECT
                cookie_id.login,
                u.permission,
                m.id,
                m.avatar
            FROM cookie_id
            LEFT JOIN users u ON (u.login = cookie_id.login)
            LEFT JOIN members m ON (m.name = cookie_id.login)
            WHERE cookie_id.id = @cookie_id@
        '''

        db = mydb.MyDB()
        sid = request.COOKIES.get('usatu_auth', '')

        if not sid:
            return

        rs = db.SqlQuery(sql, {'cookie_id': sid})
        if not rs:
            return

        self.username = rs[0]['login']
        self.permission = consts.USER_PERMISSION
        self.avatar = get_avatar(rs[0]['avatar'])

        if rs[0]['id']:
            self.user_id = rs[0]['id']
        if rs[0]['permission']:
            self.permission = rs[0]['permission']

    def get_username(self):
        return self.username

    def is_editor(self):
        return self.permission in [consts.ADMIN_PERMISSION, consts.EDITOR_PERMISSION]

    def is_admin(self):
        return self.permission in [consts.ADMIN_PERMISSION]

    def is_registered(self):
        return self.permission not in [consts.GUEST_PERMISSION]
