def get_statuses(db):
    """Returns a list of statuses in db. Requires db connection as parameter."""
    status = db.session.execute("SELECT status FROM BookStatus").fetchall()
    statuses = list()
    for i in status:
        statuses.append(i[0])
    return statuses

def check_login(session):
    """Returns True if logged in and False otherwise. Requires session as parameter"""
    if session.get("username") is None:
        return False
    else:
        return True