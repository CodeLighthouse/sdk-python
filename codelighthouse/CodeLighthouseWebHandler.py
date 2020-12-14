import requests
import json


class CodeLighthouseWebHandler:
    BASE_URL = "http://localhost:5000"
    version = "v1"
    organization_name = "\""
    x_api_key = "\""
    DEBUG = False

    def send_error(self, *args, **kwargs):
        headers = {
            "x-api-key": self.x_api_key,
            "Content-Type": "application/json",
            "organization": self.organization_name,
            "User-Agent": "CodeLighthouse"
        }

        url = f"{self.BASE_URL}/{self.version}/error"

        prepared = requests.Request("POST", url, headers=headers, data=json.dumps(kwargs))
        prepared = prepared.prepare()
        s = requests.Session()
        r = s.send(prepared)
        # integrate logger in the future
        try:
            print(f"CODELIGHTHOUSE: returned status code {r.status_code}")
            if r.status_code != 200:
                print(f'CODELIGHTHOUSE: returned message {r.json()["message"]}')
            else:
                print(f"CODELIGHTHOUSE: error_guid={r.json().get('error_guid')}")
                return r.json().get('error_guid')
        except json.decoder.JSONDecodeError as e:
            if self.DEBUG:
                print(f"JSON ERROR {e}")
            else:
                print(f"CodeLighthouse 500 JSON error")
