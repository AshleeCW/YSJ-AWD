Setup Python Virtual enviroment, place files in enviroment.

Have flask installed 

Be in flask directory htdocs/flask-app, run source/flask-app/bin/activate
Run the Server with python hello.py

Access on https://cs2s.yorkdc.net:5036
(**See below note on https and security)

Run below command to start app without using Pythons main (not recommended,not using cs2s).
FLASK_APP=hello.py flask run

Uses session variables to reuire login to access the rest of the sites. In server.py this is denoted by the @login_required annotation to call the method.
Creates hashs of the entered user passwords to store in the database.

Uses join statements to create unique profiles based on the users entered books. 
Uses LIKE concat to allow for searchs and comparisons of partial strings which allow for the likes of searching for "Dan Abnett" with entering "Dan".

Existing profile is:
	User: dog
	Password: dog
Although you can make a profile easily


Create:
	Performed on the Registration page, Add Book page, Explore Books page

Read:
	Performed on Login, Explore Books
Update:
	Performed on Settings Page for updating password
Delete:
	Performed on the Remove a Book page

Security:
	Authentication system in place for the user login which makes use of hashing  user passwords. 
	Validation of user passwords is required before any changes can be made to the existing password.
	A profile must be signed in before accessing any of the website.

	**To demonstrate a knowledge of certificates and user trust on websites I have used a self generated certificate to allow for the use of HTTPS. 
	**However most browsers will not like this but you can inspect the certificate and see it has been implemented. To remove this delete the parameter "ssl_context=('cert.pem', 'key.pem')) from the bottom of server.py 

Mobile:
	Website has been optimised for mobile users also.

Technologies used:
	HTML, CSS, Bootstrap, Python, MySQL, Jinja, Flask, WTForms. Various other libraries listed at the top of server.py

