import os, json, falcon, pyowm
from wsgiref import simple_server
from pymemcache.client.base import Client

owm = pyowm.OWM('f35186413e0abfb3c9f00ce26d54bda1') # get from https://home.openweathermap.org/api_keys
mem = Client((os.getenv('MEMCACHED_HOSTNAME', 'memcached'), 11211))

class Weather(object):
    def on_get(self, req, resp, city):
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

app = falcon.API()

app.add_route('/{city}', Weather())

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 80, app)
    httpd.serve_forever()

