import webapp2
import os
import jinja2
import logging

import passwordencrypt
import wikisignup

from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def getwiki(url):
	if not memcache.get(url):
		owikiq = db.GqlQuery("SELECT * FROM Wiki where url ='%s'"%url)
		owikiq.fetch(1)
		for owiki in owikiq:
			memcache.set(url, owiki)
	return memcache.get(url)
	
def updatewiki(url, content):
	owikiq = db.GqlQuery("SELECT * FROM Wiki where url ='%s'"%url)
	owikiq.fetch(1)
	for owiki in owikiq:
		owiki.content = content
		currver = owiki.version_count + 1
		owiki.version_count =  currver
		memcache.set(url, owiki)
		owiki.put()
		wikiversion = WikiVersions(wiki=owiki, content=content, version=currver )
		wikiversion.put()
		return owiki
	# if wiki doesn't exist create wiki
	createwiki(url, content)


	
def getallversions(main_wiki):
	wiki_history =[]
	for wikiversion in main_wiki.wiki_versions:
    		wiki_history.append('%s %s' % (wikiversion.created, wikiversion.content))
    	return wiki_history

def getversion(main_wiki, version):
	for wikiversion in main_wiki.wiki_versions:
		logging.error("wiki_ver %s wiki_ver %s version %s" %(wikiversion.content, wikiversion.version, version))	
		if (version == wikiversion.version):
    			return wikiversion.content
    			
def createwiki(url, content):
	wiki = Wiki (content=content, url=url, version_count = 1)
	wiki.put()
	memcache.set(url, wiki)
	wikiversion = WikiVersions(wiki=wiki, content=content, version=int(1))
	wikiversion.put()
	return wiki

def geturl(wiki_id):
	url = "/wiki"+wiki_id
	if wiki_id == '/':
		url = "/wiki"
	return url
		

def initialize(self) :
        cookie_value = self.request.cookies.get('user_id')
	uid_hpw = passwordencrypt.decode_cookie(cookie_value)
	self.user = None
	user = ''
	if uid_hpw:
       		self.user = uid_hpw and wikisignup.User.get_by_id(long(uid_hpw[0]))
       		user = self.user.username
       		#logging.error("view: "+self.user.username)
       	return user
       	
class Wiki (db.Model):
	content = db.TextProperty(required=True)
	url = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	version_count = db.IntegerProperty(default=int(1))
	
class WikiVersions(db.Model):
	wiki = db.ReferenceProperty(Wiki,
                                   collection_name='wiki_versions')
        created = db.DateTimeProperty(auto_now_add=True)
        content = db.TextProperty(default="")
        version = db.IntegerProperty(required=True)


class WikiFront(webapp2.RequestHandler) :
	username = ""
	def get(self):
		wiki = getwiki("wiki")
		url = "/wiki"
		if not wiki:
			#initialize db for the first and the only time
			wiki = createwiki("wiki","This is your wiki page")
		if wiki:
			self.response.out.write(render_str("wikifront.html",content=jinja2.Markup(wiki.content), wikiurl="/", user=self.username))
		else:	
			self.redirect("/wiki/_edit"+wiki_id)
	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		self.username = initialize(self)

class WikiPage(webapp2.RequestHandler) :
	username = ""
	def get(self, wiki_id) :
		content = ""
		wiki = None
		v = self.request.get("v")
		if v:
			v_n = int(v)
			url = wiki_id
			if url == "/":
				url = "wiki"
			else :
				wiki_id = wiki_id[:-1]
				url = wiki_id
			wiki = getwiki(url)
			content = getversion(main_wiki=wiki,version=v_n)
		else:
			wiki = getwiki(wiki_id)
			if wiki: 
				content = wiki.content
		if wiki:
			self.response.out.write(render_str("wikifront.html",content=jinja2.Markup(content), wikiurl=wiki_id, user=self.username))
		else:	
			self.redirect("/wiki/_edit"+wiki_id)
	
	def initialize(self, *a, **kw):
	        webapp2.RequestHandler.initialize(self, *a, **kw)
		self.username = initialize(self)

class EditWiki(webapp2.RequestHandler) :
	username = ""
	def get(self, wiki_id) :
		url = geturl(wiki_id)
		if wiki_id == "/":
			wiki_id = "wiki"
		wiki = getwiki(wiki_id)
		if self.user:
			user = self.user.username
			if wiki:
				self.response.out.write(render_str("editwiki.html",content=wiki.content, wikiurl=url, user=self.username))
			else:
				#wiki = createwiki(wiki_id, " ")
				self.response.out.write(render_str("editwiki.html",content=" ", wikiurl=url, user=self.username))
		else:
			#user should never be here without signing in
			self.redirect("/wiki")
			
	def post(self, wiki_id):
		content = self.request.get("content")
		url = geturl(wiki_id)
		if wiki_id == "/":
			wiki_id = "wiki"
		wiki = updatewiki(wiki_id, content)
		self.redirect(url)	

	def initialize(self, *a, **kw):
	        webapp2.RequestHandler.initialize(self, *a, **kw)
	        self.username = initialize(self)
	 
class HistoryPage(webapp2.RequestHandler) :
	username = ""
	def get(self, wiki_id) :
		url = wiki_id
		if wiki_id == "/":
			wiki_id = "wiki"
		wiki = getwiki(wiki_id)
		wiki_history = getallversions(wiki)
		if self.user and wiki:
			logging.error("in HistoryPage %s length=%s wiki_id = %s" %(wiki_history, len (wiki_history), wiki_id))
			user = self.user.username
			self.response.out.write(render_str("history.html",wikiversions=wiki_history, wikiurl=url, user=self.username, length=len(wiki_history)))	
		else:
			#user should never be here without signing in
			self.redirect("/wiki")	

	def initialize(self, *a, **kw):
	        webapp2.RequestHandler.initialize(self, *a, **kw)
	        self.username = initialize(self)