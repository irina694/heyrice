import cgi
import datetime

from google.appengine.ext import db
from google.appengine.api import urlfetch, taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from django.utils import simplejson
from random import randrange
from uuid import uuid4
import logging

class MainHandler(webapp.RequestHandler):
        def get(self):
                self.response.out.write(template.render('index.html', {}))
        def post(self):
                self.response.out.write(template.render('index.html', {}))

class TestHandler(webapp.RequestHandler):
        def post(self):
                self.response.out.write(template.render('markerPopup.html',{}))
        def get(self):
                self.response.out.write(template.render('markerPopup.html',{}))

class EventHandler(webapp.RequestHandler):
        def post(self):
                eventName=self.request.get('event_name')
                self.response.out.write(eventName)
class GetMarkerHandler(webapp.RequestHandler):
        def post(self):
                self.response.out.write(template.render('markerPopup.html',{}))
        def get(self):
                self.response.out.write(template.render('markerPopup.html',{}))
class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
class SubmittedEvent(DictModel):
        name = db.StringProperty(required=True)
        latitude = db.FloatProperty(required=True)
        longitude = db.FloatProperty(required=True)
        privacy = db.StringProperty(required=True)
        time = db.StringProperty(required=False)
        description = db.StringProperty(required=False)
        #tags = db.StringListProperty(required=True)
class GetEventHandler(webapp.RequestHandler):
   def get(self):
      events = SubmittedEvent.all()
      self.response.out.write(simplejson.dumps([e.to_dict() for e in events]))
class SubmitEventHandler(webapp.RequestHandler):
        def post(self):
                try:
                        #get information from the post.
                        eventName=cgi.escape(self.request.get('eventName'))
                        latStr=self.request.get('markerLat')
                        lat=float(self.request.get('markerLat'))
                        lngStr=self.request.get('markerLng')
                        lng=float(self.request.get('markerLng'))
                        privacy = self.request.get('privacy')
                        datetime = cgi.escape(self.request.get('datetime'))
                        desc = cgi.escape(self.request.get('desc'))
                        #tags = self.request.getAll('tags')
                        newEvent = SubmittedEvent(name=eventName,
                                                  latitude=lat,
                                                  longitude=lng,
                                                  privacy=privacy,
                                                  time=datetime,
                                                  description=desc)
                        db.put(newEvent)
                        self.response.out.write(template.render('index.html', {}))
                        #TODO: tags
                except:
                        self.response.out.write(template.render('index.html', {}))
                        self.response.out.write('<script type="text/javascript">alert("Event improperly formed- try again");</script>')
def main():
    
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/test',TestHandler),
                                          ('/create_event',EventHandler),
                                          ('/getMarkerPopup',GetMarkerHandler),
                                          ('/submitNewEvent',SubmitEventHandler),
                                          ('/getEvents',GetEventHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
