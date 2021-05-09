from flask import Flask
from flask import render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from os import getenv

from src.user_management.login import handle_login
from src.user_management.add_user import handle_registration
from src.services.helper_functions import get_statuses, check_login
from src.services.book_management import add_book, add_title, add_status,\
    get_books_for_user_and_status, change_book_status, change_book_holder, delete_book
from src.services.friend_management import add_friend, get_friends
from src.services.exceptions import UsernameInUse, EmptyPassword, EmptyInput,\
    DatabaseException, CredentialError, LongInput, AlreadyExistsException

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    if not check_login(session): return redirect("/login")
    try:
        books = get_books_for_user_and_status(db,session.get("username"),"")
    except DatabaseException as e:
        return render_template("index.html",message=e)
    except Exception as e:
        return render_template("index.html",message="Unexpected error: " + str(e))
    loaned = list()
    for book in books:
        if book[2] == "Loaned":
            loaned.append(book)
    friend_list = list()
    for friend in get_friends(db,session.get("username")):
        friend_list.append(friend)
    return render_template("index.html",message="Welcome "+session.get("username"),\
        books=books,loaned=loaned,statuses=get_statuses(db),friends=friend_list)


@app.route("/edit_books")
def _edit_list():
    if not check_login(session): return redirect("/login")
    try:
        books = get_books_for_user_and_status(db,session.get("username"),"")
    except DatabaseException as e:
        return render_template("index.html",message=e)
    except Exception as e:
        return render_template("index.html",message="Unexpected error: " + str(e))
    loaned = list()
    for book in books:
        if book[2] == "Loaned":
            loaned.append(book)
    friend_list = list()
    for friend in get_friends(db,session.get("username")):
        friend_list.append(friend)
    return render_template("edit_book_statuses.html",message="Welcome "+session.get("username"),\
        books=books,loaned=loaned,statuses=get_statuses(db),friends=friend_list)

@app.route("/addtitle")
def _add_title():
    if not check_login(session): return redirect("/login")
    friend_list = list()
    for friend in get_friends(db,session.get("username")):
        friend_list.append(friend)
    return render_template("addtitle.html", statuses=get_statuses(db), friends=friend_list)

@app.route("/newtitle",methods=["POST"])
def newtitle():
    if not check_login(session): return redirect("/login")
    try:
        add_title(db,request.form["author"],request.form["name"],request.form["genre"],request.form["status"])
        add_book(db,request.form["author"],request.form["name"],request.form["genre"],\
            request.form["status"],session.get("username"),request.form["friend"])
    except Exception as e:
        flash(str(e))
    else:
        flash('Book added')
    return redirect("/addtitle")

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
        return render_template("register.html",message="Username is already in use or empty."+\
            " Please choose another one")
    except EmptyPassword:
        return render_template("register.html",message="Password cannot be left empty.")
    except LongInput:
        return render_template("register.html",message="Please keep username and password at"+\
            " less than 30 characters.")
    return render_template("login.html",message="Account created. Please login with the new credentials.")

@app.route("/status")
def _status():
    if not check_login(session): return redirect("/login")
    return render_template("statuses.html",statuses=get_statuses(db))

@app.route("/add_status",methods=["POST"])
def _add_status():
    if not check_login(session): return redirect("/login")
    status = request.form["name"]
    try:
        add_status(db, status)  
    except Exception as e:
        flash(str(e))
    return redirect("/status")

@app.route("/change_status",methods=["POST"])
def change_status():
    if not check_login(session): return redirect("/login")
    if request.form["action"] == "change":
        try:
            change_book_status(db,session.get("username"),request.form,request.form["status"])
            change_book_holder(db,session.get("username"),request.form,request.form["friend"])
        except Exception as e:
            flash(str(e))
    elif request.form["action"] == "delete":
        try:
            delete_book(db,session.get("username"),request.form)
        except Exception as e:
            flash(str(e))
    return redirect("/")

@app.route("/friends")
def _friends():
    if not check_login(session): return redirect("/login")
    friends = get_friends(db, session.get("username"))
    return render_template("friends.html",friends=friends)

@app.route("/add_friend",methods=["POST"])
def _add_friend():
    if not check_login(session): return redirect("/login")
    try:
        add_friend(db,session.get("username"),request.form["name"])
    except Exception as e:
        flash(str(e))
    return redirect("/friends")
