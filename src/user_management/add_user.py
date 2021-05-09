from werkzeug.security import generate_password_hash
from src.services.exceptions import UsernameInUse, EmptyPassword

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
            query = "INSERT INTO Friends (user_id, name) VALUES"+\
                " ((SELECT id FROM Users WHERE name=:name), :me)"
            db.session.execute(query, {"name":username, "me":'me'})
            db.session.commit()
        except Exception:
            print("virhe")
    return username 
