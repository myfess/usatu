# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from app import teachers
from app import auth
from app import comments
from app import message
from app import board
from app import edu_files


def sbis_api_navigation(request):
    data = json.loads(request.body.decode('utf-8'))
    params = data['params']
    method = data['method']

    res = {}
    if method == 'board.theme_list':
        res = board.board_theme_list()
    elif method == 'edu_files.list':
        res = edu_files.edu_files_list(params)
    elif method == 'edu_files.sub_list':
        res = edu_files.edu_files_sub_list(params)
    elif method == 'edu_files.types_list':
        res = edu_files.edu_files_types_list()
    else:
        # res = {
        #     'result': False,
        #     'error_msg': 'Метод "{}" не найден'.format(method)
        # }
        raise Exception('Метод "{}" не найден'.format(method))

    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')


def api_navigation(request):
    data = json.loads(request.body.decode('utf-8'))
    params = data['data']
    method = data['method']

    # TODO: try нужен
    res = {}
    if method == 'get_chairs_struct':
        res = teachers.get_chairs_struct()
    elif method == 'sign_in':
        res = auth.sign_in(params)
    elif method == 'sign_out':
        res = auth.sign_out(request)
    elif method == 'get_comments':
        res = comments.get_comments(params)
    elif method == 'new_comment':
        res = comments.new_comment(params, request)
    elif method == 'delete_message':
        res = message.delete_message(params, request)
    elif method == 'release_message':
        res = message.release_message(params, request)
    elif method == 'get_message':
        res = message.get_message(params, request)
    elif method == 'get_message_preview':
        res = message.get_message_preview(params)
    elif method == 'write_message':
        res = message.write_message(params, request)
    elif method == 'teacher_read':
        res = teachers.teacher_read(params)
    elif method == 'teacher_write':
        res = teachers.teacher_write(params, request)
    elif method == 'release_teacher':
        res = teachers.release_teacher(params, request)
    elif method == 'delete_teacher':
        res = teachers.delete_teacher(params, request)
    else:
        res = {
            'result': False,
            'error_msg': 'Метод "{}" не найден'.format(method)
        }

    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')
