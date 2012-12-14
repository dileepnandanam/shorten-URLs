import webapp2,random

from google.appengine.ext import db


class urlmapping(db.Model):
  
  smallUrl = db.StringProperty()
  bigUrl = db.StringProperty()
  time = db.DateTimeProperty(auto_now_add=True)



class MainPage(webapp2.RequestHandler):
	
	
	def get(self):
		
		UrlIndecater=self.request.path[1:]
		if UrlIndecater:
			self.response.write( UrlIndecater)
			targets=urlmapping.all().filter("smallUrl =",UrlIndecater)
			for i in targets:
				self.redirect(str(i.bigUrl))
				break
		else:
		
			self.response.headers['content-Type'] = 'html'
			self.response.write("""<html>
				<form action="/urlstore" method="post" >
					Big url:<input name="bigUrl" >
					
					<input type=submit value="shorten" > 
				</form>
		
		
			</html>""")
	
def makeRandomID():
	
	res=urlmapping.all().order('-time').get()
	if res:
		last=str(res.smallUrl)
	else:
		last="A"
		
	res=""
	ten=True
	i=-1
	while ten:
		i+=1
		last=last[0:i]+nextc(last[i])+last[i+1:]
		if last[i]=='A':
			ten=True
			if i==len(last)-1:
				last=last+'B'
		else:
			ten=False

	return last
			
		
def nextc(c):
	return chr(65+(ord(c)+1-65)%58)
	
class UrlStore(webapp2.RequestHandler):
	
	def post(self):
		self.response.headers['content-Type'] = 'html'
		big=self.request.get('bigUrl')
		
		
		if not big:
			self.redirect("/")
			
		
		res=urlmapping.all().filter("bigUrl =",big).get()
		if res:
			small=res.smallUrl
		else:
			small=makeRandomID()
			newurl=urlmapping(smallUrl=small,bigUrl=big)
			newurl.put()
		
			
		
		
		myUrl=self.request.url.split("/")
		self.response.write(myUrl[1]+myUrl[2]+"/"+small)
		
app = webapp2.WSGIApplication([('/', MainPage),
								('/urlstore', UrlStore),('/.*', MainPage)],
															debug=True)
