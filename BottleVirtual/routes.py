"""
Routes and views for the bottle application.
"""

from bottle import route, view, run, request
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/map')
@view('map')
def about():
    """Renders the map page."""
    return dict(
        title='Drive Safely!',
        message='Drive Safely!',
        year=datetime.now().year
    )
@route('/api/<mapRoute>')
def server_api(mapRoute):
    import RouteChecker
    return RouteChecker.checkMapRoute(mapRoute)

@route('/apipost', method = 'POST')
def server_apipost():
    mapRoute = request.forms.get("mapRoute")
    import RouteChecker
    return RouteChecker.checkMapRoute(mapRoute)

@route('/api2', method = 'POST')
def server_api2():
    pointList = request.forms.get("pointList")
    import RouteChecker
    return RouteChecker.checkPointList(pointList)