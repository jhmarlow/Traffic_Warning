import requests
import time
from datetime import datetime
from threading import Timer

def get_gmaps_trip_duration(start_point, end_point, api_key):
    request_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(start_point, end_point, api_key)
    response = requests.get(request_url)
    response_json = response.json()
    duration = response_json['routes'][0]['legs'][0]['duration']['value']

    duration_inmins = duration/60
    return duration_inmins

def post_ifttt_webhook(event, value):
    ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/yh6FJ6BvybjhYSFIt-R6L'
    # payload to be sent to iftttt service
    data = {'value1':value}
    # insert our desired event
    ifttt_event_url = ifttt_webhook_url.format(event)
    # sends http post request to webhook url
    requests.post(ifttt_event_url, json=data)

api_key = 'AIzaSyBHv9_oMQrc_SdgYa_ffaZ_wrxddXNBvBo'
start_point = 'Kibworth'
end_point = 'Gaydon'
acceptable_time_inmin = 60

x=datetime.today()
y=x.replace(day=x.day, hour=21, minute=4, second=0, microsecond=0)

# delta_t=y-x
# secs=delta_t.seconds+1

secs = 1

def main():
    duration_inmins = get_gmaps_trip_duration(start_point, end_point, api_key)
    if acceptable_time_inmin < duration_inmins:
        post_ifttt_webhook('Bitcoin_price_emergency', duration_inmins)

    # # sleep for 2 mins
    # time.sleep(1*30)

t = Timer(secs, main)
t.start()