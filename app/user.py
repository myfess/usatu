# -*- coding: utf-8 -*-

from app import consts
from app import mydb


def get_avatar(avatar):
    avatar_path = None
    if avatar != 'noavatar' and avatar is not None:
        avatar_path = avatar
        if avatar_path.find('upload:') != -1:
            avatar_path = avatar_path.replace('upload:', '')
            avatar_path = consts.USATU_UPLOAD_PATH + avatar_path
        else:
            avatar_path = consts.USATU_AVATAR_PATH + avatar_path
    return avatar_path


def user_string(login):
    u = get_user_by(None, login)
    if u['id'] == '-1' or login == consts.GUEST:
        return login
    res = '{login}'.format(
        # _id=u['id'],
        login=login
    )
    return res


def get_user_by(_id=None, login=None, email=None):
    r = {
        'id': -1,
        'name': -1,
        'password': -1,
        'avatar': None,
        'email': -1
    }

    if login == consts.GUEST:
        return r

    if _id:
        where = 'id = @id@'
        p = {'id': int(_id)}
    elif login:
        where = 'name = @name@'
        p = {'name': login}
    elif email:
        where = 'email = @email@'
        p = {'email': email}
    else:
        return r

    db = mydb.MyDB()
    sql = db.sql('user_get').format(where=where)
    users = db.SqlQuery(sql, p)
    if users:
        return users[0]
    return r


def get_user_info(params, request):
    u = get_user_by(params['id'], None)
    return {
        'login': u['name'],
        'avatar': get_avatar(u['avatar'])
    }
