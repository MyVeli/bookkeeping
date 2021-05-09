from werkzeug.security import check_password_hash
from src.services.exceptions import CredentialError

def handle_login(db,username,pw):
    query = "SELECT password FROM Users WHERE name=:username"
    pw_hash = db.session.execute(query,{"username":username}).fetchone()
    if pw_hash is None:
        raise CredentialError("Wrong password or username")
    elif check_password_hash(pw_hash[0],pw):
        return username
    else:
        raise CredentialError("Wrong password or username")

