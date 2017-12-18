from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext

import json
import app.mydb as mydb
from app import consts

def get_default_context():
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
       'unentered_user': True,
       'is_editor': False, #is_editor()
       'IS_EDITOR_STR': 'false',
       'CFG_CAPTCHA_ON_STR': 'true' if consts.CAPTCHA else 'false',
       'CAPTCHA_PUBLIC': consts.CAPTCHA_PUBLIC,
       'USER_LOGIN': 'Гость',
       'USER_ID': -1
    }
    return context

def train_page(request):
    #assert isinstance(request, HttpRequest)

    db = mydb.MyDB2()
    sql = """
        SELECT * FROM vote
        """
    rs = db.SqlQuery(sql)


    data = json.dumps({'r': len(rs)})
    return HttpResponse(data, content_type='application/json')


def add_words(request):
    db = mydb.MyDB2()
    # MYUSER = mydb.auth(request, db)

    sql = """
        SELECT * FROM vote
        """
    rs = db.SqlQuery(sql)


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/test.html',
        {
            'myuser': len(rs)
        }
    )


def teachers_list(request):
    db = mydb.MyDB2()
    context = get_default_context()
    context['PAGE_TITLE'] = 'Преподаватели - '

    sql = '''
       SELECT name, id
       FROM teachers
       WHERE allow = 'yes'
       ORDER BY name
    '''
 
    rs = db.SqlQuery(sql)

    chars = []
    for r in rs:
        if len(chars) > 0 and r['name'][0] == chars[-1]['char']:
            chars[-1]['ts'].append(r)
        else:
            chars.append({
               'char': r['name'][0],
               'ts': [r]
            })

    context['chars'] = chars

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/teachers/main.html',
        context
    )
