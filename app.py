from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
#from flask_session import Session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
#Session(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    if session.get("username") == None:
        return redirect("/login")
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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/verify_credentials",methods=["POST"])
def verify_credentials():
    username = request.form["username"]
    pw = request.form["pw"]
    query = "SELECT password FROM Users WHERE name=:username"
    pw_hash = db.session.execute(query,{"username":username}).fetchone()[0]
    if pw_hash == None:
        return render_template("login.html",message="Wrong password or username.")
    elif check_password_hash(pw_hash,pw):
        session["username"] = username
    else:
        print( check_password_hash(pw_hash,pw))
        return render_template("login.html",message="Wrong password or username.")
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/login")

@app.route("/add_user",methods=["POST"])
def add_user():
    username = request.form["username"]
    pw = generate_password_hash(request.form["pw"])
    query = "SELECT id FROM Users Where name=:username"
    if db.session.execute(query, {"username":username}).fetchone() != None:
        return render_template("register.html",message="User name is already in use. Please choose another one")
    else:
        query = "INSERT INTO Users (name, password) VALUES (:name,:pw)"
        try:
            db.session.execute(query, {"name":username,"pw":pw})
            db.session.commit()
        except Exception:
            print("virhe")
    return render_template("login.html",message="Account created. Please login with the new credentials.")