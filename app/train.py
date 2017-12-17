from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext

import json
import app.mydb as mydb

def train_page(request):
    #assert isinstance(request, HttpRequest)

    db = mydb.MyDB2()
    sql = """
        SELECT * FROM vote
        """
    rs = db.query(sql)


    data = json.dumps({'r': len(rs)})
    return HttpResponse(data, content_type='application/json')
