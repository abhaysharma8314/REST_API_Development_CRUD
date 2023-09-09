from app import app

@app.route("/pcat/add")
def pcat_add():
    return "This is pcat add operation"