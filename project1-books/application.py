import os
import requests

from flask import Flask, session, request, redirect, render_template, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from passlib.hash import sha256_crypt
from flask_avatars import Avatars

#goodread  and google api key
good_key = "USE API KEY FROM GOODREADS"
google_key = "USE API KEY FROM GOOGLE BOOKS "

#login_required function
#this ensures that certain pages can only be opened by the registered user
#non-registered users are redirected to /login route
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'user_id' in session:
			return f(*args, **kwargs)
		else:
			return redirect('/login')
	return wrap

app = Flask(__name__)
avatars = Avatars(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#index route
@app.route("/")
@login_required
def index():
    return render_template("index.html")

#register route
@app.route("/register",methods = ['POST','GET'])
def register():
	if request.method == "POST":
		name = request.form.get("Name")
		username = request.form.get("Username")
		email = request.form.get('E-mail')
		password = sha256_crypt.hash(request.form.get("Password"))
		if not name or not username or not email or not password:
			flash("ONE OR MORE FIELDS ARE LEFT BLANK")
			return redirect("/register")
		if db.execute("SELECT * FROM users WHERE username = :username",{"username":username}).fetchone() != None:
			flash("USERNAME ALREADY EXISTS")
			return redirect("/register")
		else:
			db.execute("INSERT INTO users(username,name,email,password) VALUES(:username,:name,:email,:password)",{"username":username,"name":name, "email":email,"password":password})
			db.commit()
			flash("WELCOME! LOGIN IN NOW ;) ")
			return redirect("/login")
	elif request.method == "GET":
		return render_template("register.html")

#login route
@app.route("/login",methods = ['POST','GET'])
def login():
	if request.method == "POST":
		session.clear()
		username = request.form.get("username")
		password = request.form.get("password")
		if not username or not password:
			flash("USERNAME OR PASSWORD NOT ENTERED")
			return redirect("/login")
		user_info = db.execute("SELECT * FROM users WHERE username = :username",{"username":username}).fetchone()
		if user_info == None:
			flash("USER DOESN'T EXISTS")
			return redirect("/login")
		passw = user_info[4]
		if sha256_crypt.verify(password,passw):
			session["user_id"] = user_info[0]
			session["username"] = user_info[1]
			db.commit()
			return redirect("/")
		else:
			flash("INCORRECT PASSWORD :( ")
			return redirect("/login")
	elif request.method == "GET":
		return render_template("login.html")

#logout route
@app.route("/logout",methods = ['POST','GET'])
def logout():
	session.clear()
	return redirect("/")

#search route
@app.route("/search",methods = ['POST','GET'])
@login_required
def search():
	if request.method == "POST":
		search =  request.form.get("search") + '%'
		result = db.execute("SELECT * FROM books WHERE author ILIKE :search OR title ILIKE :search OR isbn ILIKE :search OR year ILIKE :search",{"search":search}).fetchall()
		if not result:
			flash("NO BOOK WITH THIS NAME")
		db.commit()
		return render_template("index.html",result=result)
	else:
		return redirect("/")

#book route
@app.route("/book/<isbn>",methods=['POST','GET'])
@login_required
def book(isbn):
	if request.method == "GET":
		book_review = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":good_key,"isbns":isbn})
		if book_review.status_code == 404:
			flash("No Such Book Exists")
			return redirect('/')
		else:
			book_review = book_review.json()
			goodread_rating = float(book_review["books"][0]["average_rating"])
			review_counts = book_review["books"][0]["reviews_count"]
			book = db.execute("SELECT * FROM books WHERE isbn =:isbn",{"isbn":isbn}).fetchone()
			reviews = db.execute("SELECT * FROM reviews WHERE book_isbn=:isbn",{"isbn":isbn}).fetchall()
			try:
				description = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn+"&key="+google_key).json()["items"][0]["volumeInfo"]["description"]
			except KeyError:
				description = "No Description Found"
		return render_template("book.html",book=book,goodread_rating=goodread_rating,description=description,review_counts=review_counts,reviews=reviews)
	elif request.method == "POST":
		review = request.form.get("review")
		rating = request.form.get("rating")
		if not review or not rating:
			flash("Review Field Empty")
			return redirect(f"/book/{isbn}")
		old_review = db.execute("SELECT * FROM reviews WHERE username=:user AND book_isbn=:isbn",{"user":session["username"],"isbn":isbn}).fetchone()
		if old_review == None:
			db.execute("INSERT INTO reviews(review,username,rating,book_isbn) VALUES(:review,:user,:rating,:isbn)",{"review":review,"user":str(session["username"]),"rating":rating,"isbn":isbn})
		else:
			db.execute("UPDATE reviews SET review=:review,rating=:rating WHERE username=:user AND book_isbn=:isbn",{"review":review,"user":session["username"],"rating":rating,"isbn":isbn})
			flash("Review Updated")
		db.commit()
		return redirect(f"/book/{isbn}")

#user route
@app.route("/user",methods=['GET'])
@login_required
def user():
	user_info = db.execute("SELECT * FROM users WHERE username=:username",{"username":session["username"]}).fetchone()
	try:
		user_review = db.execute("SELECT review,username,rating,book_isbn,title FROM reviews INNER JOIN books ON  reviews.book_isbn = books.isbn AND username=:username",{"username":session["username"]}).fetchall()
	except:
		user_review = None
	return render_template("user.html",user_review=user_review,user_info=user_info)

#api
@app.route("/api/<isbn>",methods=['POST','GET'])
def api(isbn):
	book = db.execute("SELECT * FROM books WHERE isbn =:isbn",{"isbn":isbn}).fetchone()
	if book == None:
		return jsonify({"error" : "NO SUCH BOOK EXISTS IN THIS DATABASE"}),404
	else:
		book_review = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":good_key,"isbns":isbn}).json()
		return jsonify({
		'book':book.title,
		'author':book.author,
		'isbn':book.isbn,
		'year':book.year,
		'average_rating':book_review["books"][0]["average_rating"],
		'reviews_count':book_review["books"][0]["reviews_count"]
		})
