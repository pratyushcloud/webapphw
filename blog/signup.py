import webapp2
import os
import re
import passwordencrypt
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

USERID_COOKIE = 'user_id'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_PASSWORD = re.compile(r"^.{3,20}$")
USER_EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class User (db.Model):
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	salt = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def valid_username(username):
    return USER_RE.match(username)
    
def valid_password(password):
    return USER_PASSWORD.match(password)

def valid_email(email):
    return USER_EMAIL.match(email)
	
class Signup(webapp2.RequestHandler):

  def write_form(self, error1="", error2="", error3="", error4="", username="", email=""):
 	 self.response.out.write(render_str("signup.html", error1=error1, error2 = error2, error3=error3, error4=error4, username=username, email=email))
  	 
  def get(self):
      self.write_form()
      
  def post(self):
      username = self.request.get('username')
      password = self.request.get('password')
      verify = self.request.get('verify')
      email = self.request.get('email')
      error1 = ""
      error2 = ""
      error3 = ""
      error4 = ""
      if not valid_username(username):
      	error1 = "This is not a valid user name"
      if not valid_password(password):
      	error2 = "This is not a valid password"
      if password != verify:
      	error3 = "Your password doesn't match"
      if email != "" and not valid_email(email):
      	error4 = "This is not a valid email"
      if error1 == "" and error2 == "" and error3 == "" and error4 == "":
      	encrypt = passwordencrypt.make_pw_hash(username, password)
      	#print "u=%s p=%s s=%s" %(username, encrypt[0], encrypt[1])
     	u = User(username=username, password=encrypt[0], salt=encrypt[1])
     	u.put()
     	userid = u.key().id()
     	cookie_val = passwordencrypt.make_cookie(userid,encrypt[0])
     	self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/'%(USERID_COOKIE, cookie_val))
      	self.redirect("/blog/welcome")
      else:
      	self.write_form(error1, error2, error3, error4, username, email)      
  

class Login(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(render_str("login.html", error=""))
		
      	def post(self):	
      		username = self.request.get('username')
		password = self.request.get('password')
		users = db.GqlQuery("SELECT * FROM User where username='%s'" %username)
	      	error = "Invalid Login!"
	      	if users:
	      		users.fetch(1)
	      		for user in users:
	      			if passwordencrypt.make_pw_hash1(username, password, user.salt) == user.password:
	      		   		self.redirect("/blog/welcome")
      		self.response.out.write(render_str("login.html", error=error))

class Logout(webapp2.RequestHandler) :
	def get(self) :
		self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/'%(USERID_COOKIE, ''))
      		self.redirect("/blog/signup")
      	
class Welcome(webapp2.RequestHandler):
	def get(self) :
		cookie_value = self.request.cookies.get(USERID_COOKIE)
		userid_pass = passwordencrypt.decode_cookie(cookie_value)
		u =  User.get_by_id(long(userid_pass[0]))
		if u and u.password == userid_pass[1]:
		   self.response.out.write(render_str("welcome.html", username=u.username))
		else :
		   self.redirect("/blog/signup")
  	
    	
