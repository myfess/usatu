# -*- coding: utf-8 -*-

import os

from django.shortcuts import render
from django.http import HttpRequest

from app import consts
from app import mydb
from app import auth
from app.common import get_latin_table, get_default_context, get_ID


def get_chairs_struct():
    db = mydb.MyDB()
    sql = '''
        SELECT * FROM chairs
    '''

    rs = db.SqlQuery(sql)
    faculties = []
    for r in rs:
        if r['id_parent'] == 0:
            faculties.append(r)

    for f in faculties:
        chairs = []
        for r in rs:
            if r['id_parent'] == f['id']:
                chairs.append(r)
        f['chairs'] = chairs

    res = {'faculties': faculties}
    return res


def teachers_list(request):
    db = mydb.MyDB()
    context = get_default_context(request)
    context['PAGE_TITLE'] = 'Преподаватели - '

    sql = '''
       SELECT name, id
       FROM teachers
       WHERE allow = 'yes'
       ORDER BY name
    '''

    rs = db.SqlQuery(sql)

    latin_table = get_latin_table()

    chars = []
    for r in rs:
        ch = r['name'][0]
        if chars and ch == chars[-1]['char_ru']:
            chars[-1]['ts'].append(r)
        else:
            chars.append({
                'char_ru': ch,
                'char_en': latin_table.get(ch, ch),
                'ts': [r]
            })

    context['chars'] = chars

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/teachers/main.html',
        context
    )

def teachers_add_edit(request, _id=None):
    context = get_default_context(request)

    if _id:
        context['ADDITIONAL_PARAMS'] = '''
            'teacher_id': {},
        '''.format(_id)

    return render(
        request,
        'app/teachers/add_edit.html',
        context
    )


def get_teachers_teacher(request, teacher_id=0, page=1, gotocomment=None):
    """ Карточка преподователя """

    teacher_id = int(teacher_id)
    db = mydb.MyDB()
    context = get_default_context(request)
    context['PAGE_TITLE'] = 'Преподаватели - '
    context['comments_page'] = page

    sql = '''
        SELECT
            t.*,
            c.name AS chair_name,
            c.short_name AS chair_short_name,
            f.short_name AS fc_short_name
        FROM teachers AS t
        LEFT JOIN chairs AS c ON (c.id = t.id_chair)
        LEFT JOIN chairs AS f ON (f.id = c.id_parent)
        WHERE t.id = @tid@
    '''

    ts = db.SqlQuery(sql, {'tid': teacher_id})

    if not ts:
        raise Exception('Такого преподавателя не найдено.')

    context['teacher'] = ts[0]
    context['teacher']['information'] = context['teacher']['information'].replace('\n', '<br />')
    context['teacher']['photos'] = get_teacher_photos(teacher_id)

    context['ADDITIONAL_PARAMS'] = '''
        'comments_page': {},
    '''.format(page)
    context['COMMENT_ID'] = gotocomment

    return render(
        request,
        'app/teachers/teacher.html',
        context
    )


def get_teacher_photos(teacher_id):
    """ Получение фото преподователя для карточки """

    from django.conf  import settings
    _root = getattr(settings, 'BASE_DIR', os.getcwd())
    full_path = os.path.join(_root, consts.APP_ROOT_PATH, consts.TEACHERS_PHOTO_PATH)
    full_path = os.path.abspath(full_path)
    files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

    rs = []

    for f in files:
        name, ext = os.path.splitext(f)
        tid, num = name.split('_')

        if int(tid) != teacher_id:
            continue

        if 's' in num:
            continue

        rs.append({
            'number': int(num),
            'ext': ext
        })

    rs = sorted(rs, key=lambda k: k['number'])

    res = ''
    for r in rs:
        res += '''
            <a href='{path}/{teacher_id}_{n}{ext}' target=_blank>
                <img src='{path}/{teacher_id}_{n}s{ext}' width="100" height="100" border="0" />
            </a>
        '''.format(
            path=consts.TEACHERS_PHOTO_PATH,
            teacher_id=teacher_id,
            n=r['number'],
            ext=r['ext']
        )

    return res


def teacher_read(params):
    db = mydb.MyDB()
    if not params.get('id'):
        raise Exception('Невозможно прочитать преподавателя без идентификатора')

    sql = '''
        SELECT *
        FROM teachers
        WHERE id = @id@
    '''

    rs = db.SqlQuery(sql, {'id': int(params['id'])})
    if len(rs) == 1:
        return rs[0]

    raise Exception('Преподователь не найден')


def release_teacher(params, request):
    user = auth.MyUser(request)
    if not user.is_editor():
        raise Exception('Недостаточно прав чтобы удалить сообщение')

    sql = '''
        UPDATE teachers
        SET allow = 'yes'
        WHERE id = @id@
    '''
    db = mydb.MyDB()
    db.SqlQuery(sql, {'id': int(params['id'])}, True)
    return {'result': True}


def delete_teacher(params, request):
    user = auth.MyUser(request)
    if not user.is_editor():
        raise Exception('Недостаточно прав чтобы удалить сообщение')

    sql = '''
        DELETE
        FROM teachers
        WHERE id = @id@
    '''
    db = mydb.MyDB()
    db.SqlQuery(sql, {'id': int(params['id'])}, True)
    return {'result': True}


def teacher_write(params, request):
    db = mydb.MyDB()
    user = auth.MyUser(request)
    teacher_id = int(params['id']) if params.get('id') else None

    data = {
        'name': params['name'],
        'id_chair': params['id_chair'],
        'subject': params['subject'],
        'information': params['information'],
        'fotos': params['photos']
    }

    data['fotos'] = data['fotos'] or ''
    data['information'] = data['information'] or ''

    if teacher_id is None:
        sql = '''
            INSERT
            INTO `teachers` (`id`, `name`, `id_chair`, `subject`, `information`, `fotos`, `allow`)
            VALUES (@id@, @name@, @id_chair@, @subject@, @information@, @fotos@, @allow@)
        '''

        allow = 'yes' if user.is_editor() else 'no'
        data['id'] = get_ID()
        data['allow'] = allow
        db.SqlQuery(sql, data, True)

        return {
            'result': True,
            'teacher_msg': 'Преподаватель добавится после проверки модератором.',
            'state': 'inserted'
        }
    else:
        # TODO: Если нет прав на редактирвоание - выходл - ошибка
        if not user.is_editor():
            return {
                'result': False,
                'teacher_msg': 'Нет прав изменять данные преподователя.'
            }

        sql = '''
            UPDATE teachers
            SET
                name = @name@,
                id_chair = @id_chair@,
                subject = @subject@,
                information = @information@,
                fotos = @fotos@
            WHERE id = @id@
        '''

        data['id'] = teacher_id
        db.SqlQuery(sql, data, True)

        return {
            'result': True,
            'teacher_msg': 'Данные преподавателя изменены.',
            'state': 'updated'
        }
