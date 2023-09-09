from app import app
from model.user_controller_model import model
from model.auth_model import auth_model
from config.config import dbconfig
from flask import request, send_file
from datetime import datetime
obj=model()
auth=auth_model()
@app.route("/user/getall")
@auth.token_auth()
def signup():
    return obj.user_signup_model()

@app.route("/user/addone", methods=["POST"])
@auth.token_auth()
def addone():
   return obj.user_addone_model(request.form)

@app.route("/user/addmultiple", methods=["POST"])
def addmultiple():
   return obj.user_addmultiple_model(request.json)

@app.route("/user/update", methods=["PUT"])
def update():
   return obj.user_update_model(request.form)

@app.route("/user/delete/<id>", methods=["DELETE"])
def delete(id):
   return obj.user_delete_model(id)

@app.route("/user/patch/<id>", methods=["PATCH"])
def patch(id):
   return obj.user_patch_model(request.form, id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods=["GET"])
def pagination(limit, page):
   return obj.user_pagination_model(limit, page)

@app.route("/user/<uid>/uploads/avatar", methods=["PUT"])
def upload(uid):
   file=request.files['avatar']
   uniquefilename=str(datetime.now().timestamp()).replace(".","")
   filenamesplit=file.filename.split(".")
   ext=filenamesplit[len(filenamesplit)-1]
   finalfilepath=f"uploads/{uniquefilename}.{ext}"
   file.save(finalfilepath)
   return obj.user_upload_model(uid, finalfilepath)

@app.route("/uploads/<filename>")
def get_upload(filename):
   return send_file(f"uploads/{filename}")

@app.route("/user/login", methods=["POST"])
def user_login_controller():
   return obj.user_login_model(request.form)