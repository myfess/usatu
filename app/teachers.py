# -*- coding: utf-8 -*-

import os

from django.shortcuts import render
from django.http import HttpRequest

from app import consts
from app import mydb
from app import auth
from app.common import get_latin_table, get_default_context, get_id


def get_chairs_struct(params, request):
    db = mydb.MyDB()
    rs = db.SqlQuery(db.sql('teachers_chairs'))
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

    rs = db.SqlQuery(db.sql('teachers_list'))
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


def chair_list(request, chair_id):
    """
        Список преподователей кафедры
    """

    db = mydb.MyDB()
    context = get_default_context(request)

    sql = '''
        SELECT *
        FROM chairs
        WHERE id = @id@
    '''

    chair = db.SqlQuery(sql, {'id': chair_id})

    if not chair:
        raise Exception('Такой кафедры не существеует')

    context['CHAIR_NAME'] = chair[0]['name']

    sql = '''
        SELECT
            id, name
        FROM teachers
        WHERE
            allow = 'yes'
            AND id_chair = @chair_id@
        ORDER BY name
    '''

    rs = db.SqlQuery(sql, {'chair_id': chair_id})
    context['teachers'] = rs

    return render(
        request,
        'app/teachers/chair_view.html',
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
    ts = db.SqlQuery(db.sql('teachers_teacher'), {'tid': teacher_id})

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
    full_path = os.path.join(_root, consts.FILES_PATH, consts.TEACHERS_PHOTO_PATH)
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


def teacher_read(params, request):
    db = mydb.MyDB()
    if not params.get('id'):
        raise Exception('Невозможно прочитать преподавателя без идентификатора')

    rs = db.SqlQuery(db.sql('teachers_read'), {'id': int(params['id'])})
    if len(rs) == 1:
        return rs[0]

    raise Exception('Преподователь не найден')


def release_teacher(params, request):
    user = auth.MyUser(request)
    if not user.is_editor():
        raise Exception('Недостаточно прав чтобы удалить сообщение')

    db = mydb.MyDB()
    db.SqlQuery(db.sql('teachers_release'), {'id': int(params['id'])}, True)
    return {'result': True}


def delete_teacher(params, request):
    user = auth.MyUser(request)
    if not user.is_editor():
        raise Exception('Недостаточно прав чтобы удалить сообщение')

    db = mydb.MyDB()
    db.SqlQuery(db.sql('teachers_delete'), {'id': int(params['id'])}, True)
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
        allow = 'yes' if user.is_editor() else 'no'
        data['id'] = get_id()
        data['allow'] = allow
        db.SqlQuery(db.sql('teachers_insert'), data, True)

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
        data['id'] = teacher_id
        db.SqlQuery(db.sql('teachers_update'), data, True)

        return {
            'result': True,
            'teacher_msg': 'Данные преподавателя изменены.',
            'state': 'updated'
        }
