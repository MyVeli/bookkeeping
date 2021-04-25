from werkzeug.security import generate_password_hash

def handle_registration(db,username,pw):
    query = "SELECT id FROM Users Where name=:username"
    pw_hash=generate_password_hash(pw)
    if len(username) == 0 or db.session.execute(query, {"username":username}).fetchone() != None:
        raise UsernameInUse("Username in use")
    elif len(pw) == 0:
        raise EmptyPassword("No password given")
    else:
        query = "INSERT INTO Users (name, password) VALUES (:name,:pw)"
        try:
            db.session.execute(query, {"name":username,"pw":pw_hash})
            db.session.execute("INSERT INTO Friends (name) VALUES (:me)", {"me":'me'})
            db.session.commit()
        except Exception:
            print("virhe")
    return username 

class UsernameInUse(Exception):
        pass

class EmptyPassword(Exception):
        pass