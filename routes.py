#!/usr/bin/python
# -*- coding: utf-8 -*-
# routes_in is a tuple of tuples.  The first item in each is a regexp that will
# be used to match the incoming request URL.  The second item in the tuple is
# what it will be replaced with.  This mechanism allows you to redirect incoming
# routes to different web2py locations
#
# Example: If you wish for your entire website to use init's static directory:
#
#   routes_in=( ('/static/(?P<file>[\w\./_-]+)','/init/static/\g<file>') )
#

routes_in = (
             #('.*:/','/pp4gae/'), # rewrite to pp4gae
             ('/static/(?P<file>[\w\./_-]+)','/pp4gae/static/\g<file>'),
             ('/(?P<any>.*)', '/pp4gae/default/\g<any>'),
             #'.*:/robots.txt', '/pp4gae/static/robots.txt'))
)

# routes_out, like routes_in translates URL paths created with the web2py URL()
# function in the same manner that route_in translates inbound URL paths.
#

routes_out = (
              ('/pp4gae/default/(?P<any>.*)', '/\g<any>'),
)

# Error-handling redirects all HTTP errors (status codes >= 400) to a specified
# path.  If you wish to use error-handling redirects, uncomment the tuple
# below.  You can customize responses by adding a tuple entry with the first
# value in 'appName/HTTPstatusCode' format. ( Only HTTP codes >= 400 are
# routed. ) and the value as a path to redirect the user to.  You may also use
# '*' as a wildcard.
#
# The error handling page is also passed the error code and ticket as
# variables.  Traceback information will be stored in the ticket.
#
# routes_onerror = [
#     ('init/400', '/init/default/login')
#    ,('init/*', '/init/static/fail.html')
#    ,('*/404', '/init/static/cantfind.html')
#    ,('*/*', '/init/error/index')
# ]

# specify action in charge of error handling
#
# error_handler = dict(application='error',
#                      controller='default',
#                      function='index')

# In the event that the error-handling page itself returns an error, web2py will
# fall back to its old static responses.  You can customize them here.
# ErrorMessageTicket takes a string format dictionary containing (only) the
# "ticket" key.

# error_message = '<html><body><h1>Invalid request</h1></body></html>'
# error_message_ticket = '<html><body><h1>Internal error</h1>Ticket issued: <a href="/admin/default/ticket/%(ticket)s" target="_blank">%(ticket)s</a></body></html>'
