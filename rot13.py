import webapp2
import cgi

form="""
<form method="post" >
Enter Text?
<br>
<label> 
<textarea name="text" rows="13" cols="75">%(rtext)s</textarea> 
</label>
<br> <br>
<input type ="submit">
</form>
"""

def escape_html(s):
	return cgi.escape(s, quote=True)

def rotthirteen(s):
      if s.isalpha():
       	# A-Z is 65 to 90 and a-z is 97 to 122
       	a = ord(s)
       	a13 = a + 13
       	if a < 90  and a13 < 90:
            return chr(a13)
        if a < 90 and a13 > 90:
            return chr(65+a13-90-1)
        if a < 122 and a13 < 122:
             return chr(a13)
        if a < 122 and a13 > 122:
            return chr(97+a13-122-1)
  
def rot13string(itext):
      l = len(itext)
      ctext = ""
      for i in range(0, l):
        cs = rotthirteen(itext[i])
        if cs == None:
      	   ctext = ctext + itext[i]
      	else :
      	   ctext = ctext + cs
      return ctext
      
class Rot13(webapp2.RequestHandler):

  def write_form(self, rtext=""):
 	 self.response.out.write(form %{"rtext":rtext})
  
  def get(self):
      self.write_form()

  def post(self):
      itext = self.request.get('text')
      ctext = escape_html(rot13string(itext))
      #self.response.out.write(ctext)
      self.write_form( ctext)

    	
                              
