import webapp2

from google.appengine.ext import db


class urlmapping(db.Model):
  
  smallUrl = db.StringProperty()
  bigUrl = db.StringProperty()



class MainPage(webapp2.RequestHandler):
	def get(self):
		
		UrlIndecater=self.request.get('short')
		if UrlIndecater:
			targets=urlmapping.all().filter("smallUrl =",UrlIndecater)
			for i in targets:
				self.redirect(str(i.bigUrl))
				break
		else:
		
			self.response.headers['content-Type'] = 'html'
			self.response.write("""<html>
				<form action="/urlstore" method="post" >
					Big url:<input name="bigUrl" >
					custom identifier:<input name="smallUrl" > <br>
					<input type=submit value="shorten" >
				</form>
		
		
			</html>""")
	

class UrlStore(webapp2.RequestHandler):
	
	def post(self):
		self.response.headers['content-Type'] = 'html'
		big=self.request.get('bigUrl')
		small=self.request.get('smallUrl')
		
		if not small or not big:
			self.redirect("/")
			
		same_indicators=0
		
		
		for i in urlmapping.all().filter("smallUrl =",small).run(limit=9):
			same_indicators+=1
			
		if same_indicators>0:
			self.redirect("/")
		
		
		newurl=urlmapping(smallUrl=small,bigUrl=big)
		
		newurl.put()
		myUrl=self.request.url.split("/")
		self.response.write(myUrl[1]+myUrl[2]+"/?"+"short="+small)
			
		
app = webapp2.WSGIApplication([('/', MainPage),
								('/urlstore', UrlStore)],
															debug=True)
