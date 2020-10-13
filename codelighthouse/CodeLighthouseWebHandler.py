import requests
import json


class CodeLighthouseWebHandler:
    BASE_URL = "http://localhost:5000"
    version = "v1"
    organization_name = "\""
    x_api_key = "\""

    @staticmethod
    def send_error(title: str, description: str, email: str) -> None:
        headers = {
            "x-api-key": CodeLighthouseWebHandler.x_api_key,
            "Content-Type": "application/json",
            "organization": CodeLighthouseWebHandler.organization_name
        }

        data = {
            "email": email,
            "error_title": title,
            "error": description,
        }

        url = f"{CodeLighthouseWebHandler.BASE_URL}/{CodeLighthouseWebHandler.version}/error"

        prepared = requests.Request("POST", url, headers=headers, data=json.dumps(data))
        prepared = prepared.prepare()
        s = requests.Session()
        r = s.send(prepared)
