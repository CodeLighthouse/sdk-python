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

        # ENSURE THAT THE USER DATA IS SERIALIZABLE TO JSON
        # TRY TO JSON SERIALIZE THE ENTIRE REQUEST. IF IT FAILS, IT'LL BE BECAUSE OF THE PASSED user_data.
        # CAN'T JUST TRY TO SERIALIZE THE user_data TO JSON BECAUSE IT COULD BE A NATIVE TYPE OR STRING.
        try:
            json.dumps(kwargs)
        # CATCH ERROR THROWN IF OBJECT IS NOT SERIALIZABLE
        except TypeError as e:

            # CHECK IF IT HAS AN __DICT__ ATTRIBUTE AND IF SO USE THAT
            if hasattr(kwargs['user_data'], '__dict__'):
                kwargs['user_data'] = kwargs['user_data'].__dict__

                # AFTER TRYING __DICT__, VERIFY THAT IT WORKS
                try:
                    json.dumps(kwargs)

                # IF IT DOESN'T, ASSUME IT'S NOT SERIALIZABLE
                except TypeError as e2:
                    kwargs['user_data'] = {'error': 'The passed data was not JSON-serializable'}
                    print('CODELIGHTHOUSE: additional data specified in CodeLighthouse.error() could not be serialized'
                          'to JSON. Omitting it from the report.')

            # IF NOT, ASSUME IT'S NOT SERIALIZABLE
            else:
                kwargs['user_data'] = {'error': 'The passed data was not JSON-serializable'}
                print('CODELIGHTHOUSE: additional data specified in CodeLighthouse.error() could not be serialized'
                      'to JSON. Omitting it from the report.')

        prepared = requests.Request("POST", url, headers=headers, data=json.dumps(kwargs))
        prepared = prepared.prepare()
        s = requests.Session()
        r = s.send(prepared)
        # integrate logger in the future
        try:
            print(f"CODELIGHTHOUSE: returned status code {r.status_code}")
            if r.status_code != 201:
                print(f'CODELIGHTHOUSE: returned message {r.json()["message"]}')
            else:
                print(f"CODELIGHTHOUSE: error_guid={r.json().get('error_guid')}")
                return r.json().get('error_guid')
        except json.decoder.JSONDecodeError as e:
            if self.DEBUG:
                print(f"JSON ERROR {e}")
            else:
                print(f"CodeLighthouse 500 JSON error")
