def get_statuses(db):
    status = db.session.execute("SELECT status FROM BookStatus").fetchall()
    statuses = list()
    for i in status:
        statuses.append(i[0])
    return statuses