def add_title(db,author,name,genre,status):
    """Adds a new title to the db if it's not there yet. 
    Requires db connection,author,name,genre,status as parameters"""

    query = "SELECT id FROM Title WHERE name=:name AND author=:author AND genre=:genre"
    exists = db.session.execute(query, {"name":name,"author":author,"genre":genre})
    if exists.fetchone() == None:
        query = "INSERT INTO Title (name, author, genre) VALUES (:name,:author,:genre)"
        db.session.execute(query, {"name":name,"author":author,"genre":genre})
        db.session.commit()

def add_book(db,author,name,genre,status,username):
    """Adds a book to a user. Requires the book to be in the DB as title.
    Requires db,author,name,genre,status and username as parameters."""

    query = "INSERT INTO Book (title_id, status_id, owner_id) VALUES" +\
        " ((SELECT id FROM Title WHERE author=:author AND name=:name AND genre=:genre)," +\
        "(SELECT id FROM BookStatus WHERE status=:status),(SELECT id FROM Users WHERE name=:username))"
    db.session.execute(query,{"author":author,"name":name,"genre":genre,"status":status,"username":username})
    db.session.commit()

def get_books_for_user_and_status(db,username,status):
    """Gets book author, name, status, holder & genre from DB by user and status.
    Empty string for status to get books with any status"""

    query = "SELECT author,Title.name,status,Friends.name,genre FROM  Title LEFT JOIN Book ON Title.id=Book.title_id " +\
        "LEFT JOIN BookStatus ON Book.status_id=BookStatus.id LEFT JOIN Friends ON Book.holder_id=Friends.id " +\
        "WHERE Book.owner_id=(SELECT id FROM Users WHERE name=:username"
    if status == "":
        return db.session.execute(query+")",{"username":username}).fetchall()
    query += " and status IN :status)"
    return db.session.execute(query,{"username":username,"status":status}).fetchall()

def change_book_status(db,username,titles,new_status):
    """Changes the status of books. Can update several books at one time."""
    """title = "("
    for i in titles:
        if i[0:5]=="book:":
            if len(title) != 1:
                title += ","
            title += i[5:]
    title += ")"
    if len(title) == 2:
        return"""
    title = list()
    for i in titles:
        if i[0:5]=="book:":
            title.append(i[5:])
    test = tuple(title)
    query = "UPDATE Book SET status_id = (SELECT id FROM BookStatus WHERE status=:newstatus) " +\
        "WHERE title_id IN (SELECT id FROM Title WHERE concat(author,name,genre) IN :title) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)" 
    db.session.execute(query,{"newstatus":new_status,"title":test,"username":username})
    db.session.commit()

def change_book_holder(db,username,bookname,new_holder):
    query = "UPDATE Book SET holder_id = (SELECT id FROM Friends WHERE name=:new_holder) " +\
        "WHERE title_id = (SELECT id FROM Title WHERE name=:bookname) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)"
    db.session.execute(query,{"new_holder":new_holder,"bookname":bookname,"username":username})
