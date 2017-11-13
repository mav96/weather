import pyowm
import json
import falcon
from wsgiref import simple_server
from pymemcache.client.base import Client

owm = pyowm.OWM('f35186413e0abfb3c9f00ce26d54bda1')
mem = Client(('memcached', 11211))

class Weather(object):
    def on_get(self, req, resp, city):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        weather  = {}
        result = mem.get(city)
        if not result: 
            observation = owm.weather_at_place('%s,ru' %  city)
            w = observation.get_weather()
            weather['wind'] = w.get_wind() 
            weather['humidity'] = w.get_humidity()
            weather['temperature'] = w.get_temperature('celsius')
            result = json.dumps(weather)
            mem.set(city, result, 3600)
        resp.body = result

# falcon.API instances are callable WSGI apps
app = falcon.API()

# things will handle all requests to the '/things' URL path
app.add_route('/{city}', Weather())

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 80, app)
    httpd.serve_forever()

