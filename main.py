#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import webapp2
import jinja2
import yaml
from random import choice

DOMAIN = 'saidwhat.today'

os.environ['TZ'] = 'America/Chicago'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    )

people = {}

class MainPage(webapp2.RequestHandler):
    def bail(self):
        return self.redirect('http://{}/'.format(DOMAIN))
    def get(self):
        if self.request.path != '/':
            return self.redirect('/')
        if not self.request.host.endswith(DOMAIN):
            return self.bail()

        name = self.request.host[:-len(DOMAIN)-1]
        if not name:
            return self.response.out.write(
                    jinja_environment.get_template('index.html').render(
                        {
                            }
                        )
                    )
        if '/' in name or '..' in name:
            self.bail()
        lines = people.get(name)
        if not lines:
            try:
                with open('lines/{}.yaml'.format(name)) as f:
                    people[name] = yaml.safe_load(f)
                lines = people[name]
            except (IOError, KeyError):
                return self.bail()
        self.response.out.write(
                jinja_environment.get_template('saidwhat.html').render(dict(
                    name=name.capitalize(),
                    line=choice(lines),
                    ))
                )

app = webapp2.WSGIApplication([
    ('/.*', MainPage),
], debug=True)
