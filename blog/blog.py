import os
import webapp2
import jinja2
import cgi
import datetime
import urllib
import wsgiref.handlers
import json
import time
import logging


from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

PERMA_AGE = {}
AGE = time.time()

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Blog (db.Model):
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	

class NewPostHandler(webapp2.RequestHandler):
	 
	def render(self, template, **kw):
	        self.response.out.write(render_str(template, **kw))
	

	def renderform(self, content="", subject="", error=""):
		self.render('blogpost.html', content=content, subject=subject, error=error)
	
	def get(self):
		self.renderform()
		
	def post(self):
		content = self.request.get("content")
		subject = self.request.get("subject")
		if subject and content :
			b = Blog(subject=subject, content=content)
			b.put()
			uid=b.key().id()
			self.redirect('/blog/%s' %uid)
			setblogcontent()
		else:
			error = "Both subject and title required"
			self.renderform(error=error, subject=subject, content=content)
			

class BlogHandler(webapp2.RequestHandler):
	def render(self, template, **kw):
	        self.response.out.write(render_str(template, **kw))
	        
	def renderpermalink(self, uid=0):
		b = memcache.get(str(uid))
		if not b:
			b = Blog.get_by_id(uid)
			memcache.add(str(uid), b, uid)
			PERMA_AGE[str(uid)] = time.time()
		subject= b.subject
		date = b.created
		content=b.content
		blogage = int(time.time() - PERMA_AGE[str(uid)]) 
		age = "queried %s seconds ago" %blogage
		self.render('permalink.html', content=content, subject=subject, date=date, age = age)
	
	def get(self, post_id):
		self.renderpermalink(long(post_id))
	

def setblogcontent() :
	global AGE
	logging.error('Setting blog content')
        params = {}        
    	blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")
        counter = 1
	for b in blogs:
		params['content'+str(counter)] = b.content
		params['title'+str(counter)] = b.subject
		params['date'+str(counter)] = b.created
		params['blogid'+str(counter)] = b.key().id()
		counter=counter+1
    	memcache.set('blog', params)
    	AGE = time.time()
    	logging.error("new age is = %s %s" %(AGE, memcache.get_stats()))
	return params


def blogcontentjson() :
	blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")
        params = []
	for b in blogs:
		params.append(singleblog(b))
		param = {}
	return params

def singleblog(b) :
	param = {}
	param["content"] = str(b.content)
	param["subject"] = str(b.subject)
	param["created"] = "%s-%s-%s" %(str(b.created.day), str(b.created.month), str(b.created.year)) 
	return param

class BlogFrontHandler(webapp2.RequestHandler):
	def render(self, template, **kw):
	        self.response.out.write(render_str(template, **kw))
	def get(self):
		if not memcache.get('blog'):
			setblogcontent()
		params = memcache.get('blog')
		params['age'] = "queried %s seconds ago" %int(time.time() - AGE)
		#msg = "age: %s time=%s" %(AGE, time.time())
		#self.response.out.write(msg)
		self.render('blogfront.html',**params)
	def initialize(self, *a, **kw):
	        webapp2.RequestHandler.initialize(self, *a, **kw)
    
class Flush(webapp2.RequestHandler) :		
	def get(self):
		isempty = memcache.flush_all()
		PERMA_AGE = {}
		self.redirect("/blog")
	
class JsonBlogFront(webapp2.RequestHandler) :
	def get(self):
		self.response.headers['Content-Type'] = "application/json"
		params = blogcontentjson()
		self.response.out.write(json.dumps(params))
	
class JsonBlog(webapp2.RequestHandler) :
	def get(self, post_id):
		b = Blog.get_by_id(long(post_id))
		#params = []
		#params.append(singleblog(b))
		self.response.headers['Content-Type'] = "application/json"
		self.response.out.write(json.dumps(singleblog(b)))		