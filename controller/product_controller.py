from app import app

@app.route("/product/add")
def add():
    return "This is product add operation"