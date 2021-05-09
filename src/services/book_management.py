from src.services.exceptions import EmptyInput, LongInput, DatabaseException

def add_title(db,author,name,genre,status):
    """Adds a new title to the db if it's not there yet. 
    Requires db connection,author,name,genre,status as parameters"""
    if 0 in {len(author), len(name), len(genre), len(status)}:
        raise EmptyInput("Input required for all parameters")

    query = "SELECT id FROM Title WHERE name=:name AND author=:author AND genre=:genre"
    exists = db.session.execute(query, {"name":name,"author":author,"genre":genre})
    exists = exists.fetchone()
    if exists is None:
        query = "INSERT INTO Title (name, author, genre) VALUES (:name,:author,:genre)"
        try:
            db.session.execute(query, {"name":name,"author":author,"genre":genre})
            db.session.commit()
        except Exception as e:
            DatabaseException("Unexpected database error: "+str(e))

def add_book(db,author,name,genre,status,username,holder):
    """Adds a book to a user. Requires the book to be in the DB as title.
    Requires db,author,name,genre,status and username as parameters."""
    
    if 0 in {len(author), len(name), len(genre), len(status), len(username), len(holder)}:
        raise EmptyInput("Input required for all parameters")

    query = "INSERT INTO Book (title_id, status_id, owner_id, holder_id) VALUES" +\
        " ((SELECT id FROM Title WHERE author=:author AND name=:name AND genre=:genre)," +\
        "(SELECT id FROM BookStatus WHERE status=:status),(SELECT id FROM Users WHERE name=:username),"+\
        "(SELECT id FROM Friends WHERE name=:holder and user_id=(SELECT id FROM Users WHERE name=:name2)))"
    try:
        db.session.execute(query,{"author":author,"name":name,"genre":genre,"status":status,\
            "username":username,"holder":holder,"name2":username})
        db.session.commit()
    except Exception as e:
        raise DatabaseException("Unexpected database error: "+str(e))

def get_books_for_user_and_status(db,username,status):
    """Gets book author, name, status, holder & genre from DB by user and status.
    Empty string for status to get books with any status"""
    if len(username) == 0:
        raise EmptyInput("Input required for all parameters")

    query = "SELECT author,Title.name,status,Friends.name,genre FROM  Title LEFT JOIN Book ON Title.id=Book.title_id " +\
        "LEFT JOIN BookStatus ON Book.status_id=BookStatus.id LEFT JOIN Friends ON Book.holder_id=Friends.id " +\
        "WHERE Book.owner_id=(SELECT id FROM Users WHERE name=:username"
    if status == "":
        try:
            return db.session.execute(query+")",{"username":username}).fetchall()
        except Exception as e:
            raise atabaseException("Unexpected database error: "+str(e))
    query += " and status IN :status)"
    try:
        return db.session.execute(query,{"username":username,"status":status}).fetchall()
    except Exception as e:
        raise DatabaseException("Unexpected database error: "+str(e))

def change_book_status(db,username,titles,new_status):
    """Changes the status of books. Can update several books at one time."""
    if 0 in {len(username), len(titles), len(new_status)}:
        raise EmptyInput("Input required for all parameters")
    title = titles_from_formlist(titles)
    if len(title) == 0:
        return
    query = "UPDATE Book SET status_id = (SELECT id FROM BookStatus WHERE status=:newstatus) " +\
        "WHERE title_id IN (SELECT id FROM Title WHERE concat(author,name,genre) IN :title) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)" 
    try:
        db.session.execute(query,{"newstatus":new_status,"title":title,"username":username})
        db.session.commit()
    except Exception as e:
        raise DatabaseException("Unexpected database error: "+str(e))

def change_book_holder(db,username,titles,new_holder):
    """Changes the holder of books. Can update several at one time."""
    title = titles_from_formlist(titles)
    if len(title) == 0:
        return
    elif len(new_holder) == 0:
        raise EmptyInput("Input required for all parameters")
    query = "UPDATE Book SET holder_id = (SELECT id FROM Friends WHERE name=:new_holder and user_id="\
        "(SELECT id FROM Users WHERE name=:name)) " +\
        "WHERE title_id IN (SELECT id FROM Title WHERE concat(author,name,genre) IN :title) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)"
    try:
        db.session.execute(query,{"new_holder":new_holder,"name":username,"title":title,"username":username})
        db.session.commit()
    except Exception as e:
        raise DatabaseException("Unexpected database error: "+str(e))

def delete_book(db, username, titles):
    """Deletes books from user. Can delete several at one time."""
    title = titles_from_formlist(titles)
    if len(title) == 0:
        return
    query = "DELETE FROM Book WHERE title_id IN "+\
        "(SELECT id FROM Title WHERE concat(author,name,genre) IN :title) and owner_id = " +\
        "(SELECT id FROM Users WHERE name=:username)"
    try:
        db.session.execute(query,{"name":username,"title":title,"username":username})
        db.session.commit()
    except Exception as e:
        raise DatabaseException("Unexpected database error: "+str(e))


def titles_from_formlist(form_list):
    """Returns a tuple with books. Picks items starting with "book:" from given array."""
    title_list = list()
    for i in form_list:
        if i[0:5]=="book:":
            try:
                title_list.append(i[5:])
            except IndexError:
                raise IndexError("Invalid booklist")
    return tuple(title_list)

def add_status(db, status):
    """Adds a new status to database"""
    if len(status) == 0:
        raise EmptyInput("Please add status name.")
    elif len(status) > 15:
        raise LongInput("Please keep status to less than 15 characters.")
    query = "INSERT INTO BookStatus (status) VALUES (:status)"
    try:
        db.session.execute(query,{"status":status})
        db.session.commit()
    except Exception as e:
        raise DatabaseException("Status already in the system")

