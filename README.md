# bookkeeping

Bookkeeping is a system for keeping track of books owned and loaned. It is easy to forget having loaned a book to a friend and who currently has what book. It can also be used to keep an inventory of books, listing books not yet read and having a wishlist for books.

Functionalities:
* The user can sign in and register a new user account
* The user can add new book titles to the system
* The user can assign and remove genres and keywords to the books
* The user can add new genres and keywords to the system
* The user can change the status of a book (e.g. read, on wishlist, loaned, to be read, currently reading)
* The user can add the names of their friends to the system
* The user can mark books as being loaned to or from one of their friends
* The user can list and search books in the system based on title, genre, person or status

Current state:
* registration, login and logout have been implemented
* it's possible to add new books to the system and visibility is restricted by user account
* it's possible to add new statuses and genres
* User can add friends
* User can loan books to friends 
* User can change the status of books
* UI is missing styling and thus very rough

<br>
Testing:<br>
heroku link: 
https://tsohabookkeeping.herokuapp.com/ <br>
Register a new account, login with it. From the index page you can add new status, book or friend.