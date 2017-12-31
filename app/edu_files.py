# -*- coding: utf-8 -*-

import time
import json

from django.shortcuts import render

from app import mydb
from app import auth
from app import consts
from app.common import get_default_context, epoch_to_date_str, get_ID
from app.common import get_records_set_json, json_to_record


def edu_files_types_list():
    db = mydb.MyDB()

    sql = '''
        SELECT
            ft.id,
            ft.type
        FROM files_types ft
        WHERE
        EXISTS (
            SELECT 1
            FROM files
            WHERE
            files.type = ft.id::text
            AND files.allow = 'yes'
        )
        ORDER BY ft.type ASC
    '''

    rs = db.SqlQuery(sql)

    d = [[r['id'], r['type']] for r in rs]
    s = [
        {'n': 'id', 't': 'Число целое'},
        {'n': 'type', 't': 'Строка'}
    ]
    return get_records_set_json(s, d)


def edu_files_list(params):
    db = mydb.MyDB()

    rec = json_to_record(params['Фильтр'])
    subject_id = rec.get('subject')
    type_id = rec.get('type')
    d = []
    s = []

    ps = {}
    cond = ''

    if type_id:
        cond = ' AND files.type = @type@ '
        ps['type'] = type_id

    if subject_id:
        sql = '''
            SELECT
                files.id,
                files.ext,
                files.description,
                files_types.type,
                files.size,
                files.time,
                files.author
            FROM files
            LEFT JOIN files_types ON (files_types.id = files.type::int)
            WHERE
                files.allow = 'yes'
                AND files.subject = (@subject@)::text
                {cond}
            ORDER BY files.time DESC
        '''.format(
            cond=cond
        )

        ps['subject'] = subject_id
        rs = db.SqlQuery(sql, ps)

        for r in rs:
            d.append([
                r['id'], r['ext'], r['description'], r['type'],
                int(r['size'] // 1024),
                epoch_to_date_str(r['time']),
                r['author']
            ])

        s = [
            {'n': 'id', 't': 'Число целое'},
            {'n': 'ext', 't': 'Строка'},
            {'n': 'description', 't': 'Строка'},
            {'n': 'type', 't': 'Строка'},
            {'n': 'size', 't': 'Число целое'},
            {'n': 'time', 't': 'Строка'},
            {'n': 'author', 't': 'Строка'}
        ]

    else:
        sql = '''
            SELECT
                fs.id,
                fs.subject,
                count(*) AS _count
            FROM files f
            LEFT JOIN files_subjects fs ON (fs.id = f.subject::int)
            WHERE
                f.allow = 'yes'
            GROUP BY fs.id, fs.subject
            ORDER BY subject
        '''
        rs = db.SqlQuery(sql)

        d = [[r['id'], r['subject'], r['_count']] for r in rs]

        s = [
            {'n': 'id', 't': 'Число целое'},
            {'n': 'subject', 't': 'Строка'},
            {'n': 'count', 't': 'Число целое'}
        ]
    return get_records_set_json(s, d)


def edu_files_sub_list(params):
    db = mydb.MyDB()

    sql = '''
        SELECT
            f.type AS id,
            ft.type
        FROM files f
        LEFT JOIN files_types ft ON (ft.id = f.type::int)
        WHERE
            f.subject = (@subject@)::text
            AND f.allow = 'yes'
        GROUP BY f.type, ft.type
        ORDER BY ft.type
    '''

    rs = db.SqlQuery(sql, {'subject': params['subject_id']})

    d = [[r['id'], r['type']] for r in rs]

    s = [
        {'n': 'id', 't': 'Число целое'},
        {'n': 'type', 't': 'Строка'},
    ]
    return get_records_set_json(s, d)


def get_files_for_edu_main(request, subject=None, type_id=None):
    context = get_default_context(request)
    db = mydb.MyDB()

    #  Заполняем шаблон правильным случаем, в зависимости от переданных параметров

    bread_crumbs = [{'text': 'USATU.com', 'link': '/'}]
    context['RIGHT_MENU'] = False

    if not subject:
        bread_crumbs.append({'text': 'Файлы для учёбы', 'last': True})
        context['BREAD_CRUMBS'] = json.dumps(bread_crumbs)
        context['SUBJECT_ID'] = 'null'
        context['TYPE_ID'] = 'null'
    elif not type_id:
        sql = '''
            SELECT subject
            FROM files_subjects
            WHERE id = @id@
        '''
        subject_name = db.SqlQueryScalar(sql, {'id': int(subject)})
        bread_crumbs.append({'text': 'Файлы для учёбы', 'link': '/files_for_edu/'})
        bread_crumbs.append({'text': subject_name, 'last': True})
        context['BREAD_CRUMBS'] = json.dumps(bread_crumbs)
        context['SUBJECT_ID'] = int(subject)
        context['TYPE_ID'] = 'null'
        context['RIGHT_MENU'] = True
    else:
        sql = '''
            SELECT
                ( SELECT subject FROM files_subjects WHERE id = @sid@ ) AS subject,
                ( SELECT type FROM files_types WHERE id = @tid@ ) AS type
        '''
        names = db.SqlQuery(sql, {
            'sid': int(subject),
            'tid': int(type_id)
        })

        bread_crumbs.append({'text': 'Файлы для учёбы', 'link': '/files_for_edu/'})
        bread_crumbs.append({
            'text': names[0]['subject'],
            'link': '/files_for_edu/{}'.format(int(subject))
        })
        bread_crumbs.append({'text': names[0]['type'], 'last': True})

        context['BREAD_CRUMBS'] = json.dumps(bread_crumbs)
        context['SUBJECT_ID'] = int(subject)
        context['TYPE_ID'] = int(type_id)

    context['ENABLE_ADD_FILE'] = consts.ENABLE_ADD_FILE
    return render(
        request,
        'app/files_for_edu/main.html',
        context
    )


def get_files_for_edu_add_file(request):
    context = get_default_context(request)
    db = mydb.MyDB()
    user = auth.MyUser(request)

    bread_crumbs = [
        {'text': 'USATU.com', 'link': '/'},
        {'text': 'Файлы для учёбы', 'link': '/files_for_edu/'},
        {'text': 'Добавить свой файл', 'last': True}
    ]
    context['BREAD_CRUMBS'] = json.dumps(bread_crumbs)

    description = request.POST.get('ft_description', '')
    type_id2 = int(request.POST.get('fd_type', -1))
    type2 = request.POST.get('ft_type', '')
    subject = int(request.POST.get('fd_subject', -1))
    subject2 = request.POST.get('ft_subject', '')
    author = request.POST.get('ft_author', '')
    submit_upload = request.POST.get('submit_upload', None)

    settings = {}

    if not submit_upload:
        context['FILE_SETTINGS'] = json.dumps(settings)
        return render(
            request,
            'app/files_for_edu/add_file.html',
            context
        )

    # upload_tmp_name = isset($_FILES["upload"]["tmp_name"]) ? $_FILES["upload"]["tmp_name"] : "";
    # upload_name = isset($_FILES["upload"]["name"]) ? $_FILES["upload"]["name"] : "";
    # upload_size = isset($_FILES["upload"]["size"]) ? (int)$_FILES["upload"]["size"] : 0;

    _file = request.FILES['upload'] # this is my file
    upload_tmp_name = ''
    upload_name = 'test.zip'
    upload_size = 100

    upload_result = {
        'was_add': False,
        'was_upload': False,
        'was_bad_ext': False,
        'was_add_mod': False,
        'no_subject': False,
        'no_type': False,
    }

    inserted = False

    if is_uploaded_file(upload_tmp_name):
        upload_result['was_upload'] = True
        ext = GetExt(['.zip', '.rar'], upload_name)
        if ext == -1:
            upload_result['was_bad_ext'] = True
        else:
            subject_id = get_subject(subject, subject2)
            type_id = get_type(type_id2, type2)

            if subject_id is None:
                upload_result['no_subject'] = True
            if type_id is None:
                upload_result['no_type'] = True

            if not upload_result['no_subject'] and not upload_result['no_type']:
                ext = ext.lower()
                ID = get_ID()
                path = consts.DOCS_PATH + ID + ext

                if copy(upload_tmp_name, path):
                    sql = '''
                        INSERT INTO files VALUES(
                            @id@, @ext@, @subject_id@, @description@, @type_id@,
                            @size@, @author@, @uploader@, @allow@, @time@
                        )
                    '''

                    ps = {
                        'id': ID,
                        'ext': ext,
                        'subject_id': subject_id,
                        'description': description,
                        'type_id': type_id,
                        'size': upload_size,
                        'author': author,
                        'uploader': user.username,
                        'allow': 'yes' if user.is_editor() else 'no',
                        'time': int(time.time())
                    }

                    db.SqlQuery(sql, ps, True)
                    inserted = True
                    upload_result['was_add'] = user.is_editor()
                    upload_result['was_add_mod'] = not user.is_editor()

    if submit_upload:
        settings['upload_result'] = upload_result

        if  not inserted:
            settings['description'] = description
            settings['author'] = author
            settings['subject_text'] = subject2
            settings['type_text'] = type2
            settings['subject_id'] = int(subject)
            settings['type_id'] = int(type_id2)

    context['FILE_SETTINGS'] = json.dumps(settings)
    return render(
        request,
        'app/files_for_edu/add_file.html',
        context
    )


def is_uploaded_file(_file):
    # TODO:
    return False


def copy(p1, p2):
    # TODO:
    return False


def GetExt(exts, name):
    """
        Args:
            exts - массив допустимых расширений в нижнем регистре,
            name - имя файла

        Returns:
            либо найденное расширение в том регистре в котором оно в name либо -1 если не нашли
    """

    for ext in exts:
        if name[len(ext) * (-1)].lower() == ext:
            return ext
    return -1


def get_subject(subject_id, subject_text):
    db = mydb.MyDB()
    if subject_id != 0 and subject_id != -1:
        return int(subject_id)

    if subject_text == '':
        return None

    sql = '''
        SELECT id
        FROM files_subjects
        WHERE subject = @subject@
    '''

    rs = db.SqlQuery(sql, {'subject': subject_text})
    if len(rs) == 1:
        return int(rs[0]['id'])

    sql = '''
        INSERT INTO files_subjects (subject)
        VALUES (@subject@)
        RETURNING "id"
    '''
    last_id = db.SqlQueryScalar(sql, {'subject': subject_text})
    return last_id


def get_type(type_id, type_text):
    db = mydb.MyDB()
    if type_id != 0 and type_id != -1:
        return int(type_id)

    if type_text == '':
        return None

    sql = '''
        SELECT id
        FROM files_types
        WHERE type = @type@
    '''

    rs = db.SqlQuery(sql, {'type': type_text})
    if len(rs) == 1:
        return int(rs[0]['id'])

    sql = '''
        INSERT INTO files_types (type)
        VALUES (@type@)
        RETURNING "id"
    '''
    last_id = db.SqlQuery(sql, {'type': type_text})
    return last_id
