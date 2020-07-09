from flask import Flask, Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flaskext.mysql import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flaskext.mysql import MySQL
from userform import *
from errors import *
from flask_login import LoginManager, UserMixin
from functools import wraps
import MySQLdb
import hashlib, os


booky = Flask(__name__)

#should place this in .env file and be random
booky.config['SECRET_KEY'] = 'Something About a Rainbow and a Green Island'
conn = MySQLdb.connect("", "", "","")

cursor = conn.cursor()

bootstrap = Bootstrap(booky)

@booky.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.register.data:
        return redirect(url_for('register'))
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        key = hash(password)
        saltQuery = ("SELECT userPassword FROM users where userName = %s")
        
        query = ("SELECT * FROM users WHERE userName = %s AND userPassword = %s")
        data = (name, key)
        cursor.execute(query, data)
        account = cursor.fetchone()
        if not cursor.rowcount:
            flash('Incorrect username or password')
        else:
            session['logged_in'] = True
            session['name'] = name
            return redirect(url_for('getData'))
    else:
        return render_template('index.html', form=form)
    return render_template('index.html', form=form, name=session.get('name'))

@booky.route('/logout')
def logout():
    #clear sessions for new login
    session.pop('logged_in', None)
    session.pop('name', None)
    return redirect(url_for('index'))

#Check if user is logged in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('index'))
    return wrap

@booky.route('/register', methods=['GET', 'POST'])
def register():
    salt = os.urandom(32)
    form = RegisterForm()
    if form.validate_on_submit():   
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if password != form.passwordConf.data:
            flash('Those passwords did not match!')
        else:
            key = hash(password)
       
            query = ("INSERT INTO users (userName, userEmail, userPassword) VALUES (%s, %s, %s)")
            data = (name, email, key)
            cursor.execute(query, data)
            conn.commit()
            
    return render_template('register.html', form=form)

@booky.route('/results', methods=['GET', 'POST'])
@login_required
def getData():
    cursor.execute('SELECT user_picture FROM users WHERE userName = %s', [session.get('name')])
    picture = cursor.fetchone()
    conn.commit() 
    cursor.execute('SELECT userName, userEmail FROM users')
    result = cursor.fetchone()
    username = session.get('name')
   # USERID = ('SELECT userId FROM users WHERE userName = ')
    cursor.execute('''SELECT users.userid, book.book_name AS "Book Name", author
                        FROM users_book
                            JOIN users ON users_book.userId = users.userId
                            JOIN book ON users_book.book_id = book.book_id
                        WHERE author IS NOT NULL
                            AND users.userName = %s''',[username])
    result = cursor.fetchall()
    conn.commit()

    return render_template('user.html', picture=picture, result=result)

@booky.route('/search_books', methods=['GET', 'POST'])
@login_required
def searchBook():
    form = SearchBookForm()
    result = ""
    if form.submit1.data and form.validate():
        author_search = form.author.data
        cursor.execute("SELECT book_id, book_name, author FROM book WHERE author LIKE '{}'".format("%" + author_search + "%"))
        result = cursor.fetchall()
        conn.commit()
    addBook = AddBookToUserForm()
    if addBook.submit2.data and addBook.validate():
        if addBook.validate_on_submit():
            bookId = addBook.bookId.data
            cursor.execute("SELECT userId FROM users WHERE userName = %s", [session.get('name')])
            userId = cursor.fetchone()
            cursor.execute('INSERT INTO users_book (userId, book_id) VALUES (%s, %s)', [userId, bookId])
            conn.commit()
    return render_template('search_book.html', form=form, result=result, addBook=addBook)

@booky.route('/add_book', methods=['GET', 'POST'])
@login_required
def addBook():
    form = AddBookForm()
    if form.validate_on_submit():
        name = form.bookname.data
        author = form.author.data
        query = ("INSERT INTO book (book_name, author) VALUES (%s, %s)")
        data = (name, author)
        cursor.execute(query, data)
        conn.commit()
    return render_template('add_book.html', form = form)

@booky.route('/delete_book', methods=['GET', 'POST'])
@login_required
def deleteBook():
    form = DeleteBook()
    if form.validate_on_submit():
        bookId = form.bookId.data
        cursor.execute("SELECT userId FROM users WHERE userName = %s", [session.get('name')])
        userId = cursor.fetchone()
        cursor.execute('DELETE FROM users_book WHERE (userId, book_id) = (%s, %s)', [userId, bookId])
        conn.commit() 
    return render_template('delete_book.html', form=form)

@booky.route('/update_user', methods=['GET', 'POST'])
@login_required
def updateUser():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        cursor.execute("SELECT userId FROM users WHERE userName = %s", [session.get('name')])
        userId = cursor.fetchone()
        old = form.oldPassword.data
        new = form.newPassword.data
        confirm = form.confirmPassword.data
        if new == confirm:
            hashed_old = hash(old)
            cursor.execute("SELECT * FROM users WHERE userPassword = %s", [hashed_old])
            if cursor.rowcount >= 1:
                cursor.execute("UPDATE users SET userPassword = %s WHERE userId = %s", [hash(new), userId])
            else:
                flash("That password is incorrect")
        else:
            flash("Those passwords didn't match")
    return render_template('update_user.html', form=form)


#ERROR HANDLING****************************

@booky.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@booky.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__=='__main__':
    booky.run(host='cs2s.yorkdc.net', port=5036, debug=True, ssl_context=('cert.pem', 'key.pem'))
