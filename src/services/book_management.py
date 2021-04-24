def add_title(db,author,name,genre,status):
    query = "SELECT id FROM Title WHERE name=:name AND author=:author AND genre=:genre"
    exists = db.session.execute(query, {"name":name,"author":author,"genre":genre})
    if exists.fetchone() == None:
        query = "INSERT INTO Title (name, author, genre) VALUES (:name,:author,:genre)"
        db.session.execute(query, {"name":name,"author":author,"genre":genre})
        db.session.commit()

def add_book(db,author,name,genre,status,owner_id):
    query = "INSERT INTO Book (title_id, status_id, owner_id) VALUES" +\
        " ((SELECT id FROM Title WHERE author=:author AND name=:name AND genre=:genre)," +\
        "(SELECT id FROM BookStatus WHERE status=:status),:owner_id)"
    db.session.execute(query,{"author":author,"name":name,"genre":genre,"status":status,"owner_id":owner_id})
    db.session.commit()

"""Gets books from DB by user and status. Empty string for status to get books with any status"""
def get_books_for_user_and_status(db,username,status):
    query = "SELECT author,Title.name,status,Friends.name FROM  Title LEFT JOIN Book ON Title.id=Book.title_id " +\
        "LEFT JOIN BookStatus ON Book.status_id=BookStatus.id LEFT JOIN Friends ON Book.holder_id=Friends.id " +\
        "WHERE Book.owner_id=(SELECT id FROM Users WHERE name=:username"
    if status == "":
        return db.session.execute(query+")",{"username":username}).fetchall()
    query += " and status IN :status)"
    return db.session.execute(query,{"username":username,"status":status}).fetchall()

def change_book_status(db,username,bookname,new_status):
    query = "UPDATE Book SET status_id = (SELECT id FROM BookStatus WHERE status=:newstatus) " +\
        "WHERE title_id = (SELECT id FROM Title WHERE name=:bookname) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)"
    db.session.execute(query,{"newstatus":new_status,"bookname":bookname,"username":username})

def change_book_holder(db,username,bookname,new_holder):
    query = "UPDATE Book SET holder_id = (SELECT id FROM Friends WHERE name=:new_holder) " +\
        "WHERE title_id = (SELECT id FROM Title WHERE name=:bookname) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)"
    db.session.execute(query,{"new_holder":new_holder,"bookname":bookname,"username":username})
