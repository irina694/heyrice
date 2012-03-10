import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


class MainHandler(webapp.RequestHandler):
        def get(self):
                self.response.out.write(template.render('index.html', {}))
        def post(self):
                self.response.out.write(template.render('index.html', {}))
class TestHandler(webapp.RequestHandler):
        def post(self):
                self.response.out.write("Test Post Completed!")
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/test',TestHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
