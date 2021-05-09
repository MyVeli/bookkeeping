from src.services.exceptions import DatabaseException, EmptyInput, LongInput, AlreadyExistsException

def add_friend(db, username, name):
    if len(name) > 30:
        raise LongInput("Please use under 30 character names")
    elif len(name) == 0:
        raise EmptyInput("No name added")
    query = "SELECT id FROM Friends WHERE user_id=(SELECT id FROM Users WHERE name=:username)"+\
        " AND name=:name"
    result = db.session.execute(query,{"username":username,"name":name}).fetchone()
    if result is not None:
        raise AlreadyExistsException("Friend with this name already added")
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
