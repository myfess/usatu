# -*- coding: utf-8 -*-
import time
import hashlib
import random
import re
import uuid
from email.utils import parseaddr

from django.template.loader import render_to_string
from django.shortcuts import render

from app import consts
from app import mydb
from app.user import get_avatar, get_user_by
from app.common import my_mail


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


def auth(auth_login):
    db = mydb.MyDB()
    sid = md5(get_rand_string())
    db.SqlQuery(
        db.sql('auth_sign_in'),
        {'cookie_ID': sid, 'auth_login': auth_login},
        True
    )
    return sid


def get_permissions(login):
    db = mydb.MyDB()
    ps = db.SqlQuery(db.sql('auth_permissions'), {'login': login})
    if len(ps) != 1:
        return consts.USER_PERMISSION
    return ps[0]['permission']


def auth_sign_out(sid):
    db = mydb.MyDB()
    db.SqlQuery(db.sql('auth_sign_out'), {'cookie_id': sid}, True)
    return True


def auth_sign_in(login, password):
    if login == '' or login == consts.GUEST_IPB:
        return {'token': None, 'msg': 'Недопустимый логин'}

    user = get_user_by(None, login)
    if user['id'] == -1:
        return {'token': None, 'msg': 'Нет пользователя с таким логином'}

    password = md5(password)
    if password != user['password']:
        return {'token': None, 'msg': 'Неверный пароль'}

    token = auth(login)
    return {'token': token}


def restore_pass(params, request):
    """
        Заявка на восстановлние пароля
    """

    sql = '''
        INSERT
        INTO members_restore_pass (member_id, secret, dt)
        VALUES (@member_id@, @secret@, NOW() at time zone 'UTC')
    '''

    secret = uuid.uuid4()
    user = get_user_by(email=params['email'])
    member_id = user['id']

    if member_id < 1:
        return {'msg': 'Email не найден'}

    db = mydb.MyDB()
    db.SqlQuery(sql, {'member_id': member_id, 'secret': secret}, True)

    email = user['email']
    if not email or email == -1:
        raise Exception('Пустой Email')

    tpl = render_to_string('app/email/restore_pass.html')
    tpl = tpl.format(
        LOGIN=user['name'],
        DOMEN=consts.DOMEN,
        NAV_CAPTION=consts.NAV_CAPTION,
        SECRET=secret
    )

    subject = 'Восстановление пароля'
    my_mail(subject, tpl, email)

    return {'result': True}


def restore_change_pass(params, request):
    """
        Смена пароля
    """

    db = mydb.MyDB()
    secret = uuid.UUID(params['secret'])
    new_pass = params['password']
    if len(new_pass) < 4:
        return {'msg': 'Пароль не может быть короче 4 символов.'}
    new_pass = md5(new_pass)

    sql = '''
        SELECT member_id
        FROM members_restore_pass
        WHERE
            secret = @secret@
            AND (NOW() at time zone 'UTC' - dt) < interval '1 day'
    '''

    rs = db.SqlQuery(sql, {'secret': secret})

    if not rs:
        return {'msg': 'Неверная ссылка для восстановления, возможно она устарела, получите новую.'}

    mid = rs[0]['member_id']

    sql = '''
        UPDATE members
        SET password = @password@
        WHERE id = @mid@
        RETURNING id, name, email
    '''

    rs = db.SqlQuery(sql, {'mid': mid, 'password': new_pass})

    if not rs:
        raise Exception('Не удалось сменить пароль')

    tpl = render_to_string('app/email/password_changed.html')
    tpl = tpl.format(
        LOGIN=rs[0]['name'],
        DOMEN=consts.DOMEN,
        NAV_CAPTION=consts.NAV_CAPTION
    )
    subject = 'Пароль изменён'
    my_mail(subject, tpl, rs[0]['email'])
    return {'result': True}



def get_registration(request):
    context = get_default_context(request)
    return render(
        request,
        'app/auth/registration.html',
        context
    )


def get_restore_password(request, secret=None):
    context = get_default_context(request)

    if secret:
        context['secret'] = str(uuid.UUID(secret))

        return render(
            request,
            'app/auth/change_password.html',
            context
        )

    return render(
        request,
        'app/auth/restore_password.html',
        context
    )


def registraion(params, request):
    """
        Регистрация нового пользователя
    """

    db = mydb.MyDB()

    new_pass = params['password']
    email = params['email']
    login = params['login']

    if '@' not in parseaddr(email)[1]:
        return {'msg': 'Вы ввели неверный email.'}

    if len(new_pass) < 4:
        return {'msg': 'Пароль не может быть короче 4 символов.'}

    new_pass = md5(new_pass)

    pattern = re.compile('^[a-zA-Z0-9-_]+$')
    if not pattern.match(login):
        msg = (
            'В имене пользователя используются недопустимые символы. '
            'Используйте латинские буквы, цифры, подчеркивание или тире'
        )
        return {'msg': msg}

    sql = '''
        SELECT count(*)
        FROM members
        WHERE email = @email@
    '''

    email_count = db.SqlQueryScalar(sql, {'email': email})
    if email_count:
        return {'msg': 'Пользователь с указанным email-ом уже зарегистрирован.'}

    sql = '''
        SELECT count(*)
        FROM members
        WHERE name = @login@
    '''

    login_count = db.SqlQueryScalar(sql, {'login': login})
    if login_count:
        return {'msg': 'Пользователь с указанным именем уже зарегистрирован.'}

    sql = '''
        INSERT
        INTO members (id, name, password, email)
        VALUES (
            (SELECT max(m.id) + 1 FROM members m),
            @name@, @password@, @email@
        )
        RETURNING id, name, email
    '''

    rs = db.SqlQuery(sql, {
        'name': login,
        'password': new_pass,
        'email': email,
    })

    if not rs:
        raise Exception('Не удалось зарегистрироваться')

    tpl = render_to_string('app/email/registered.html')
    tpl = tpl.format(
        LOGIN=rs[0]['name'],
        DOMEN=consts.DOMEN,
        NAV_CAPTION=consts.NAV_CAPTION
    )
    subject = 'Вы зарегистрировались'
    my_mail(subject, tpl, rs[0]['email'])

    return {'result': True}


class MyUser:
    username = consts.GUEST
    permission = consts.GUEST_PERMISSION
    user_id = consts.GUEST_ID
    avatar = None

    def __init__(self, request):
        db = mydb.MyDB()
        sid = request.COOKIES.get('usatu_auth', '')

        if not sid:
            return

        rs = db.SqlQuery(db.sql('auth_user'), {'cookie_id': sid})
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


def get_default_context(request):
    user = MyUser(request)

    context = {
        'ADS': consts.ADS,
        'COUNTERS': consts.COUNTERS,
        'JIVOSITE': consts.JIVOSITE,
        'REFORMAL': consts.REFORMAL,
        'SAPE': consts.SAPE,
        'TYPESCRIPT': consts.TYPESCRIPT,
        'ES5': consts.ES5,
        'USATU_PATH': consts.USATU_PATH,
        'PRODUCTION_STR': 'true' if consts.PRODUCTION else 'false',
        'ADDITIONAL_PARAMS': '',
        'unentered_user': not user.is_registered(),
        'is_editor': user.is_editor(),
        'IS_EDITOR_STR': 'true' if user.is_editor() else 'false',
        'CFG_CAPTCHA_ON_STR': 'true' if consts.CAPTCHA_ON else 'false',
        'CAPTCHA_PUBLIC': consts.CAPTCHA_PUBLIC,
        'USER_LOGIN': user.username,
        'AVATAR': mark_safe("'{}'".format(user.avatar)) if user.avatar else 'null',
        'USER_ID': user.user_id,
        'COMMENT_ID': None,
        'NAV_CAPTION': consts.NAV_CAPTION,
        'DOMEN': consts.DOMEN,
        'LEFT_MENU': True,
        'HIGHLOAD': False
    }
    return context
