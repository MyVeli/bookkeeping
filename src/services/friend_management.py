def add_friend(db, username, name):
    if len(name) > 30:
        return
    query = "INSERT INTO Friends (user_id,name) VALUES ((SELECT id FROM Users" +\
        " WHERE Users.name=:username), :name)"
    db.session.execute(query,{"username":username,"name":name})
    db.session.commit()

def get_friends(db,username):
    query = "SELECT name FROM Friends WHERE user_id=(SELECT id FROM Users WHERE name=:username)"
    result =  db.session.execute(query,{"username":username}).fetchall()
    friends = list()
    for i in result:
        friends.append(i[0])
    return friends
