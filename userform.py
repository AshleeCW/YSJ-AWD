from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators =[DataRequired()], render_kw={"placeholder": "Need a value, even for register. Current bug."})
    password = PasswordField('What is your Password?', validators =[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Submit')
    register = SubmitField('Register')

class RegisterForm(FlaskForm):
    name = StringField('What is your name?', validators =[DataRequired()])
    email = StringField('Enter your email address', validators =[DataRequired()])
    password = PasswordField('Enter a password', validators =[DataRequired()])
    passwordConf = PasswordField('Confirm  your password', validators =[DataRequired()])
    submit = SubmitField('Submit')

class AddBookForm(FlaskForm):
    bookname = StringField('Enter the name of the book', validators =[DataRequired()])
    author = StringField('Enter the name of the author(s)', validators =[DataRequired()])
    submit = SubmitField('Submit')

class SearchBookForm(FlaskForm):
    author = StringField('Enter the name of the author to search the database for')
    submit1 = SubmitField('Submit')

class AddBookToUserForm(FlaskForm):
    bookId = IntegerField('Enter ID of the book you want to add to your profile')
    submit2 = SubmitField('Submit')

class DeleteBook(FlaskForm):
    bookId = IntegerField('Enter the ID of the book you want to delete from your profile')
    bookName = StringField('Enter the name of the book for confirmation')
    submit = SubmitField('Submit')

class UpdatePasswordForm(FlaskForm):
    oldPassword = PasswordField('Enter your current password', validators=[DataRequired()])
    newPassword = PasswordField('Enter a new password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm your new password', validators=[DataRequired()])
    submit = SubmitField('Submit')
