# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from app import teachers
from app import auth
from app import comments
from app import message
from app import board
from app import edu_files
from app import cache
from app import user

from app.common import json_dumps


allowed_api_functions = {
    'get_chairs_struct': 'teachers',
    'sign_in': 'auth',
    'sign_out': 'auth',
    'get_comments': 'comments',
    'new_comment': 'comments',
    'delete_message': 'message',
    'release_message': 'message',
    'get_message': 'message',
    'get_message_preview': 'message',
    'write_message': 'message',
    'teacher_read': 'teachers',
    'teacher_write': 'teachers',
    'delete_teacher': 'teachers',
    'release_teacher': 'teachers',
    'get_user_info': 'user',

    'registraion': 'auth',
    'restore_change_pass': 'auth',
    'restore_pass': 'auth'
}


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

    res = json_dumps(res)
    return HttpResponse(res, content_type='application/json')


def api_navigation(request):
    data = json.loads(request.body.decode('utf-8'))
    params = data['data']
    method_name = data['method']
    res = call_method(method_name, params, request)
    return HttpResponse(res, content_type='application/json')


def get_cache(method_name, params, request):
    cache_api_functions = [
        'get_chairs_struct',
        'get_user_info'
    ]

    if method_name in cache_api_functions:
        cached, result = cache.cache_check(method_name, params)
        if cached:
            # Попали в кэш
            return result
        # Не попали в кэш
        err, result = my_call_user_func(method_name, params, request)
        if not err:
            cache.cache_add(method_name, params, result)
        return result
    err, result = my_call_user_func(method_name, params, request)
    return result


def my_call_user_func(method_name, params, request):
    try:
        module_name = allowed_api_functions[method_name]
        module = globals()[module_name]
        method_to_call = getattr(module, method_name)
        result = method_to_call(params, request)
        return False, json_dumps(result)
    except Exception as e:
        r = {
            'result': False,
            'error_msg': str(e)
        }
        return True, json_dumps(r)


def call_method(method_name, params, request):
    if method_name in allowed_api_functions:
        return get_cache(method_name, params, request)
    r = {
        'result': False,
        'error_msg': 'Вызываемый метод не входит в API'
    }
    return json_dumps(r)
