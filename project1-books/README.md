# Project 1

Web Programming with Python and JavaScript

The App is named infinity|book|reviews

How to Run:-
* Run `pip3 install -r requirements.txt` in your terminal window to make sure that all of the necessary Python packages (Flask and SQLAlchemy, for instance) are installed.
* Visit the PostgreSQL [https://docs.cs50.net/web/2020/x/projects/1/project1.html](https://docs.cs50.net/web/2020/x/projects/1/project1.html) for steps to setup Database.
* Use the  database credentials from the `Heroku PostgreSQL add-on` settings section to get the `DATABASE URI` and create and environment variable named `DATABASE_URL`
* Use the  database credentials from the `Heroku PostgreSQL add-on` settings section to login in to [https://adminer.cs50.net/](https://adminer.cs50.net/).
* Copy commands from [create-database.txt](create-database.txt) and use `SQL Command` in [https://adminer.cs50.net/](https://adminer.cs50.net/) to create the `tables`
* Run `python import.py` to import all the books from [books.csv](books.csv) to the database
* Add **API Keys** from `Goodreads API` and `Google Books API` in [application.py](application.py)
* Set the environment variable `FLASK_APP` to be `application.py` and `DEBUG` to `True`.
* Run `flask run` to start the server.

## Templates

1. <ins>register.html</ins> : This page asks user for 'Name','Username'(unique),'Email','Password' to regitser.These are submitted by a from to the "/register" route in "application.py".

2. <ins>login.html</ins> : This page asks users to for 'Username' and 'Password' to login.These are submitted by a form to "/login" routein "application.py".

3. <ins>index.html</ins> : This page searches for a book.The page has a search bar which submits the 'search by user' to the "/search" route.The "/search" route return a table for all possible matching if found, otherwise 'flashes' error message. The user can then click on the book name in the table to go to the book page.

4. <ins>book.html</ins> : This page displays the basic information about the book Title, Author, ISBN, Year of Publication, Cover Image(using OpenLibrary API), Description(using Google Books API), Rating Bar(using Goodreads API) and Number of Reviews(using Goodreads API).The page also allows user to submit a review and a rating out of 5 and display the reviews by users.

5. <ins>users.html</ins> : This page diplays user information Name, Email, Username and all the reviews he submitted on the webisite.The route also displays a profile picture for user(robohash).

6. <ins>layout.html</ins> : This page is the baisc layout of the web-app. All the other html pages extends this page.

## static
 * <ins>"style.css"</ins> : the page contains all the styling for each webpage. I used SASS to write CSS. The web-app also uses Bootstrap.


## application.py

* <ins>/</ins> : This route returns "index.html".

* <ins>/register</ins> :  This route registers the user to the web-app. The password is converted to an hash using "sha256_crypt" function of passlib library. The name, username , email and password submitted by the user is stored in the "users" tables.If the user submits any field as empty in "register.html" an error message is flashed and user is redirected to "/register" route.

* <ins>/login</ins> : This route logs in a user.The route first verify whether the user exists or not.If the user exists it usees "sha256_crypt.verify()" function from passlib to verfiy the user's password and start a session for the user. If the user doesn't exists or password is incorrect, the user is redirected to "/login" route and an error message is flashed.

* <ins>/logout</ins> : This route clears the session of the logged in user and redirects to "/" route.

* <ins>/search</ins> : This route searches for a book in the "books" table and returns the result and redirect to "index.html". If the book doesn't exists or not found in "books" table an error message is flashed.

* <ins>/book/<isbn></ins> : This route displays books information and also submits user review. If the request is GET this route querys for book information from "books" table and user review from "reviews" table. The route searches for book description from "Google Books API" and rating + reviews from "Goodreads API". If the request is POST the route stores the user review of the book in "reviews" table; if the review exists it updates the old review and redirects to "/book/<isbn>" route.

* <ins>/user</ins> : This route returns user information and their reviews to "user.html".

* <ins>/api/<isbn></ins> : This route returns a JSON object that conatins the book information and rating+review(from Goodreads).
