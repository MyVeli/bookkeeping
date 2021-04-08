from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:hUnajamel00N1@localhost:5432/bookkeeping_db"
db = SQLAlchemy(app)

@app.route("/")
def index():
    print("testi")
    books = db.session.execute("SELECT author,name FROM Title")
    return render_template("index.html",message="Tervetuloa!",items=books)

@app.route("/addtitle")
def add_title():
    status = db.session.execute("SELECT status FROM BookStatus")
    return render_template("addtitle.html", statuses=status)

@app.route("/newtitle",methods=["POST"])
def newtitle():
    owner_id = 1
    add_title(request.form["author"],request.form["name"],request.form["genre"],request.form["status"])
    if request.form["add"] == "True":
        add_book(request.form["author"],request.form["name"],request.form["genre"],request.form["status"],owner_id)
    return redirect("/")

def add_title(author,name,genre,status):
    query = "SELECT id FROM Title WHERE name=:name AND author=:author AND genre=:genre"
    exists = db.session.execute(query, {"name":name,"author":author,"genre":genre})
    if exists.fetchone() == None:
        query = "INSERT INTO Title (name, author, genre) VALUES (:name,:author,:genre)"
        db.session.execute(query, {"name":name,"author":author,"genre":genre})
        db.session.commit()

def add_book(author,name,genre,status,owner_id):
    query = "INSERT INTO Book (title_id, status_id, owner_id) VALUES" +\
        " ((SELECT id FROM Title WHERE author=:author AND name=:name AND genre=:genre)," +\
        "(SELECT id FROM BookStatus WHERE status=:status),:owner_id)"
    db.session.execute(query,{"author":author,"name":name,"genre":genre,"status":status,"owner_id":owner_id})
    db.session.commit()

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    pw = request.form["pw"]
    
    session["username"] = username
    return

@app.route("/register",methods=["POST"])
def register():
    return

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/adduser",methods=["POST"])
def add_user():
    username = request.form("username")
    pw = generate_password_hash(request.form("password"))
    query = "SELECT id FROM Users Where name=:username"
    if db.session.execute(query, {"username":username}) != None:
        return redirect("/register")
    else:
        query = "INSERT INTO Users (name, password) VALUES {:username,:pw}"
        db.session.execute(query, {"username":username,"password":pw})