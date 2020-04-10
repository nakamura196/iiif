import requests
import sys
import yaml

class Notify:
    @classmethod
    def send(self, message, path):

        with open(path) as file:
            yml = yaml.load(file, Loader=yaml.SafeLoader)

        url = "https://notify-api.line.me/api/notify"
        token = yml["token"]
        headers = {"Authorization" : "Bearer "+ token}
        payload = {"message" :  message}

        requests.post(url ,headers = headers ,params=payload)