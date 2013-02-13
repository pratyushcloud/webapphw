
import webapp2

import helloworld.helloworld
import helloworld.hellotemplate

WIKI_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([('/', 'helloworld.helloworld.HelloWorld') 
				,('/rot13','rot13.Rot13')
				,('/signup','signup.Signup')
				,('/welcome','signup.Welcome')
				,('/blog/newpost','blog.blog.NewPostHandler')
				,('/blog/([0-9]+)','blog.blog.BlogHandler')
				,('/blog','blog.blog.BlogFrontHandler')
				,('/blog/signup', 'blog.signup.Signup')
				,('/blog/welcome', 'blog.signup.Welcome')
				,('/blog/login', 'blog.signup.Login')
				,('/blog/logout', 'blog.signup.Logout')
				,('/blog/.json', 'blog.blog.JsonBlogFront')
				,('/blog/([0-9]+).json', 'blog.blog.JsonBlog')
				,('/blog/flush','blog.blog.Flush')
				,('/wiki','wiki.wiki.WikiFront')
				,('/wiki/signup','wiki.wikisignup.WikiSignup')
				,('/wiki/login','wiki.wikisignup.WikiLogin')
				,('/wiki/logout','wiki.wikisignup.WikiLogout')
				,('/wiki/_edit(/(?:[a-zA-Z0-9_-]+/?)*)' , 'wiki.wiki.EditWiki')
				,('/wiki/_history(/(?:[a-zA-Z0-9_-]+/?)*)', 'wiki.wiki.HistoryPage')
                ,('/wiki(/(?:[a-zA-Z0-9_-]+/?)*)', 'wiki.wiki.WikiPage')
                ,('/jobc','jobc.jobc.MainPage')
                ,('/jobc/home','jobc.jobc.PostLoginPage')
                ,('/jobc/inviteonly/', 'jobc.jobc.InviteOnly')
                ,('/jobc/_edit/realjd(/(?:[a-zA-Z0-9_-]+/?)*)', 'jobc.jobc.ReadlJDEdit')
                ,('/jobc/realjd(/(?:[a-zA-Z0-9_-]+/?)*)', 'jobc.jobc.ReadlJD')
				#,('/hellotemplate','helloworld.hellotemplate.HelloTemplate')
				#,('/sign', 'helloworld.hellotemplate.Guestbook')
				],
                              debug=True)