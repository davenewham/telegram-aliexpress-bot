import json
import random
import requests

from backports.configparser import ConfigParser


class RebrandlyApi(object):
    def __init__(self):
        self._read_config()

    def _read_config(self):
        """Reads the config file with the Rebrandly API key"""
        import os
        file_path = os.path.join(os.path.dirname(__file__), './config.ini')
        config = ConfigParser()
        config.read(file_path)
        self._apikey = config.get('Rebrandly', 'apikey')

    def get_short_url(self, url, slashtag):
        """Shortens the given url and uses the slashtag in the short url"""
        while True:
            request = requests.post("https://api.rebrandly.com/v1/links",
                              data=json.dumps({
                                  "destination": url
                                  , "domain": {"fullName": "rebrand.ly"}
                                  , "slashtag": slashtag + self._generate_random_id()
                              }),
                              headers={
                                  "Content-type": "application/json",
                                  "apikey": self._apikey
                              })

            if request.status_code == requests.codes.ok:
                result = request.json()
                return result["shortUrl"], result["id"]

    @staticmethod
    def _generate_random_id():
        return '{0:07}'.format(random.randint(1, 10000000))

    # TODO: Implement link delete
