import mysql.connector
import json
from flask import make_response
from datetime import datetime
from config.config import dbconfig
from datetime import timedelta
import jwt
class model():
    def __init__(self):
            try:
                self.con=mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
                self.con.autocommit=True
                self.cur=self.con.cursor(dictionary=True)
                print("connection successfull")
            except:
                print("some error")

    def user_signup_model(self):
        self.cur.execute("SELECT * FROM users")
        result=self.cur.fetchall()
        if len(result)>0:
             res=make_response({"payload":result})
             res.headers['Access-Control-Allow-Origin']='*'
             return res
        else:
             return make_response({"message":"No data"}, 204)
    
    def user_addone_model(self, data):
         self.cur.execute(f"INSERT INTO users(NAME, EMAIL, role_id, password) VALUES('{data['NAME']}','{data['EMAIL']}','{data['role_id']}','{data['phone']}') ")
         print(data['EMAIL'])
         return make_response({"message":"created successfully"}, 201)
    
    def user_update_model(self, data):
         self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', role_id='{data['role_id']}' WHERE id='{data['id']}")
         if self.cur.rowcount>0:
              return make_response({"message":"updated successfully"}, 201)
         else:
              return make_response({"message":"Nothing to update"}, 202)
         
    def user_delete_model(self, id):
         self.cur.execute(f"DELETE FROM users WHERE id={id}")
         if self.cur.rowcount>0:
              return make_response({"message":"deleted successfully"}, 200)
         else:
              return make_response({"message":"Nothing to delete"}, 202)
         
    def user_patch_model(self, data, id):
         qry="UPDATE users SET "
         for key in data:
              qry+=f"{key}='{data[key]}',"
         qry=qry[:-1] + f" WHERE id={id}"
         self.cur.execute(qry)
         if self.cur.rowcount>0:
              return make_response({"message":"updated successfully"}, 201)
         else:
              return make_response({"message":"Nothing to update"}, 202)  
    
    def user_pagination_model(self, limit, page):
         limit=int(limit)
         page=int(page)
         start=(page*limit)-limit
         qry=f"SELECT * FROM users LIMIT {start}, {limit}"
         self.cur.execute(qry)
         result=self.cur.fetchall()
         if len(result)>0:
             res=make_response({"payload":result, "page_no":page,"limit":limit})
             res.headers['Access-Control-Allow-Origin']='*'
             return res
         else:
             return make_response({"message":"No data"}, 204)
         
    def user_upload_model(self,uid, filepath):
         self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
         if self.cur.rowcount>0:
              return make_response({"message":"updated successfully"}, 201)
         else:
              return make_response({"message":"Nothing to update"}, 202)
         
    def user_login_model(self, data):
         self.cur.execute(f"SELECT id, name, email, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
         result=self.cur.fetchall()
         userdata=result[0]
         exp_time=datetime.now() + timedelta(minutes=15)
         exp_epoch_time=int(exp_time.timestamp())
         payload={
              "payload":userdata,
              "exp":exp_epoch_time
         }
         jwttoken=jwt.encode(payload, "ABHAY", algorithm="HS256")
         return make_response({"token":jwttoken}, 200)
         
    def user_addmultiple_model(self, data):
         qry="INSERT INTO users(NAME, EMAIL, role_id, password) VALUES"
         for userdata in data:
              qry += f"('{userdata['NAME']}','{userdata['EMAIL']}','{userdata['role_id']}','{userdata['password']}'),"
         finalqry=qry.rstrip(",")
         self.cur.execute(finalqry)   
         return make_response({"message": "users created successfully"}, 201)