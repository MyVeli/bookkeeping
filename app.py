from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

from src.user_management.login import handle_login, CredentialError
from src.user_management.add_user import handle_registration, UsernameInUse, EmptyPassword
from src.services.helper_functions import get_statuses
from src.services.book_management import add_book,add_title, get_books_for_user_and_status
from src.services.friend_management import add_friend, get_friends

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    username = session.get("username")
    if username == None:
        return redirect("/login")
    books = get_books_for_user_and_status(db,username,"")
    loaned = list()
    for book in books:
        if book[2] == "Loaned":
            loaned.append(book)
    return render_template("index.html",message="Welcome "+session.get("username"),books=books,loaned=loaned)

@app.route("/addtitle")
def _add_title():
    return render_template("addtitle.html", statuses=get_statuses(db))

@app.route("/newtitle",methods=["POST"])
def newtitle():
    owner = session.get("username")
    if owner == None:
        redirect("/login")
    status = request.form["status"]
    owner_id = db.session.execute("SELECT id FROM Users WHERE name=:name",{"name":owner}).fetchone()[0]
    add_title(db,request.form["author"],request.form["name"],request.form["genre"],request.form["status"])
    if request.form["add"] == "True":
        add_book(db,request.form["author"],request.form["name"],request.form["genre"],request.form["status"],owner_id)
    return redirect("/")

@app.route("/login")
def _login():
    return render_template("login.html")

@app.route("/verify_credentials",methods=["POST"])
def verify_credentials():
    username = request.form["username"]
    pw = request.form["pw"]
    try:
        username = handle_login(db,username,pw)
    except CredentialError:
        return render_template("login.html",message="Wrong password or username.")
    session["username"] = username
    return redirect("/")

@app.route("/register")
def _register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/login")

@app.route("/add_user",methods=["POST"])
def add_user():
    try:
        handle_registration(db,request.form["username"],request.form["pw"])
    except UsernameInUse:        
        return render_template("register.html",message="Username is already in use or empty. Please choose another one")
    except EmptyPassword:
        return render_template("register.html",message="Password cannot be left empty.")
    return render_template("login.html",message="Account created. Please login with the new credentials.")

@app.route("/status")
def _status():
    return render_template("statuses.html",statuses=get_statuses(db))

@app.route("/add_status",methods=["POST"])
def add_status():
    status = request.form["name"]
    query = "INSERT INTO BookStatus (status) VALUES (:status)"
    try:
        db.session.execute(query,{"status":status})
        db.session.commit()
    except:
        return redirect("/new_status")
    return redirect("/status")

@app.route("/friends")
def _friends():
    friends = get_friends(db, session.get("username"))
    return render_template("friends.html",friends=friends)

@app.route("/add_friend",methods=["POST"])
def _add_friend():
    add_friend(db,session.get("username"),request.form["name"])
    return redirect("/friends")
