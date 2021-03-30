#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_NODE_NAME = 'default_node'
DEFAULT_COUNT_NAME = 10


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def node_key(node_name=DEFAULT_NODE_NAME):
    """Constructs a Datastore key for a Node Data entity.

    We use node_name as the key.
    """
    return ndb.Key('NodeName', node_name)


class NodeData(ndb.Model):
    """A main model for representing a data from sensor."""
    sensor_id = ndb.StringProperty(indexed=True)
    data = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        node_name = self.request.get('node_name', DEFAULT_NODE_NAME)
        data_count = self.request.get('data_count', DEFAULT_COUNT_NAME)
        node_query = NodeData.query(
            ancestor=node_key(node_name)).order(-NodeData.date)
        node_data_list = node_query.fetch(10)

        template_values = {
            'node_data': node_data_list,
            'node_name': urllib.quote_plus(node_name),
            'data_count': data_count,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START readdata]
class ReadData(webapp2.RequestHandler):

    def get(self):
        node_name = self.request.get('node_name', DEFAULT_NODE_NAME)
        data_count = self.request.get('data_count')
        data_only = self.request.get('data_only')
        count = DEFAULT_COUNT_NAME
        if data_count is not None and data_count != '':
            count = int(data_count)
        node_query = NodeData.query(
            ancestor=node_key(node_name)).order(-NodeData.date)
        node_data_list = node_query.fetch(count)

        if data_only is not None and data_only == '1':
            self.response.write(node_data_list)
            return

        template_values = {
            'node_data': node_data_list,
            'node_name': urllib.quote_plus(node_name),
            'data_count': count,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END readdata]


# [START nodedata]
class UploadData(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        node_name = self.request.get('node_name', DEFAULT_NODE_NAME)
        record = NodeData(parent=node_key(node_name))

        record.data = self.request.get('upload_data')
        record.sensor_id = self.request.get('sensor_id')
        record.put()

        query_params = {'node_name': node_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END nodedata]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadData),
    ('/readdata', ReadData),
], debug=True)
# [END app]
