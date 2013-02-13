import webapp2
import cgi
import re

form="""
<form method="post">
<b>Welcome to Signup Page </b><br> <br>
<label> Username </label><input type="text" name="username" value=%(username)s>

<div style="color: red">%(error1)s</div>
</br>
<label> Password <input type="password" name="password" >
</label>
<div style="color: red">%(error2)s</div>
</br>
<label> Verify Password <input type="password" name="verify">
</label>
<div style="color: red">%(error3)s</div>
</br>
<label> Email (optional) <input type="text" name="email" value=%(email)s>
</label>
<div style="color: red">%(error4)s</div>
</br>
<input type="Submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_PASSWORD = re.compile(r"^.{3,20}$")
USER_EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
    
def valid_password(password):
    return USER_PASSWORD.match(password)

def valid_email(email):
    return USER_EMAIL.match(email)

def escape_html(s):
	return cgi.escape(s, quote=True)
	
class Signup(webapp2.RequestHandler):

  def write_form(self, error1="", error2="", error3="", error4="", username="", email=""):
 	 self.response.out.write(form %{"error1":error1, "error2":error2, "error3":error3,"error4":error4, "username":escape_html(username), "email":escape_html(email)})
  
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
      	self.redirect("/welcome?username=%s" %username)
      else:
      	self.write_form(error1, error2, error3, error4, username, email)      
  
      

class Welcome(webapp2.RequestHandler):
	def get(self) :
		self.response.out.write("Welcome, "+ self.request.get('username')+"!");
	
    	
