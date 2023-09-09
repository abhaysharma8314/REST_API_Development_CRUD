import mysql.connector
import json
from flask import make_response, request
from datetime import datetime
from config.config import dbconfig
from datetime import timedelta
import jwt
import re
from functools import wraps
class auth_model():
    def __init__(self):
            try:
                self.con=mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
                self.con.autocommit=True
                self.cur=self.con.cursor(dictionary=True)
                print("connection successfull")
            except:
                print("some error")
    
    def token_auth(self,endpoint=""):
         def inner1(func):
              @wraps(func)
              def inner2(*args):
                endpoint=request.url_rule
                authorization=request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                     token=authorization.split(" ")[1]
                     try:
                       jwtdecoded=jwt.decode(token, "ABHAY", algorithms="HS256")
                     except jwt.ExpiredSignatureError:
                         return make_response({"Error":"Token_Expired"}, 401)
                     role_id = jwtdecoded['payload']['role_id']
                     self.cur.execute(f"SELECT * FROM accessibility_view WHERE endpoint='{endpoint}'")
                     result = self.cur.fetchall()
                     if len(result)>0:
                         allowed_roles=json.loads(result[0]["roles"])
                         if role_id in allowed_roles:
                             return func(*args)
                         else:
                             return make_response({"error":"Invalid role"}, 404)
                     else:
                         return make_response({"Error":"Unknown Endpoint"},404)
                else:
                     return make_response({"Error":"Invalid_Token"},401)
                
              return inner2
         return inner1