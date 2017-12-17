from django.conf import settings
from django.db import connections

import json
import time
import hashlib
import random

class MyDB2:
   def __init__(self):
      self.cursor = connections['default'].cursor()
      
   def query(self, sql, no_result=False):
      try:
         if len(sql) == 0:
            return list()

         self.cursor.execute(sql)

         if no_result:
            #self.cursor.commit()
            return None

         columns = [column[0] for column in self.cursor.description]
         results = []
         for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
         return results
      except Exception as e:
         print('Ошибка выполнение запроса: {err}'.format(err=str(e)))


def escape(s):
    s = s.replace("`", "\\`")
    s = s.replace("\\", "\\\\")
    return s

def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()

def get_rand_string(_id):
    _seed = int(time.time()) ^ int(_id)
    random.seed(_seed)
    digi = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
            "A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V","W","Y","Z",
            "a","b","c","d","e","f","g","h","j","k","l","m","n","p","q","r","s","t","u","v","w","y","z"]
    res = ""
    n = len(digi)
    
    for i in range(50):
        res += digi[random.randint(0, n - 1)]
    return res

def auth(request, db):
    user = {"id": 0,
            "islogin": False,
            "login": "Guest", 
            "permission": "g"}

    sid = escape(request.COOKIES.get('sid', ""))
    sql = """ 
        SELECT u.id, u.login, u.permission
        FROM cookies AS c 
        LEFT JOIN users AS u ON (u.id = c.user_id)
        WHERE c.cookie = '{sid}' """.format(sid=sid)
    r = db.query(sql)

    if len(r) > 0:
        user["id"] = int(r[0]["id"])
        user["islogin"] = True
        user["login"] = r[0]["login"]
        user["permission"] = r[0]["permission"]

    return user
