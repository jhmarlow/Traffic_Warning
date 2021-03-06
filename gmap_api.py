import requests
import time
from datetime import datetime
from threading import Timer

def get_gmaps_trip_duration(start_point, end_point, api_key):
        """Get .json file from google maps api.

        Arguments:
                start_point {str} -- name of location
                end_point {str} -- name of location
                api_key {str} -- key  

        return {float} - journey duration in mins
        """
        request_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(start_point, end_point, api_key)
        response = requests.get(request_url)
        response_json = response.json()
        duration = response_json['routes'][0]['legs'][0]['duration']['value']

        duration_inmins = duration/60
        return duration_inmins

def post_ifttt_webhook(event, value):
        """Create webhook using IFTTT app.
        
        Arguments:
                event {str} -- name of event create using IFTTT
                value {int} -- duration of journey
        """
        ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/yh6FJ6BvybjhYSFIt-R6L'
        # payload to be sent to iftttt service
        data = {'value1':value}
        # insert our desired event
        ifttt_event_url = ifttt_webhook_url.format(event)
        # sends http post request to webhook url
        requests.post(ifttt_event_url, json=data)

def set_timer():
        """Create timer for when to check gmaps.

        Returns:
                secs {int} -- time in secs for next run

        """
        x=datetime.today()
        y=x.replace(day=x.day, hour=6, minute=30, second=0, microsecond=0)
        delta_t=y-x
        secs=delta_t.seconds+1
        return secs

def main(start_point, end_point, acceptable_time_inmin):
        """Run the main function.
        
        Arguments:
                start_point {[type]} -- [description]
                end_point {[type]} -- [description]
                acceptable_time_inmin {[type]} -- [description]
        """
        api_key = 'AIzaSyBHv9_oMQrc_SdgYa_ffaZ_wrxddXNBvBo'
        duration_inmins = get_gmaps_trip_duration(start_point, end_point, api_key)
        if acceptable_time_inmin < duration_inmins:
                post_ifttt_webhook('Traffic update', duration_inmins)

# Run 
t = Timer(set_timer(), main('Kibworth', 'Gaydon', 60))
t.start()