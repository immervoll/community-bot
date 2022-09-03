from tkinter import E


class API():
    _api_host : str
    _api_token : str
    
    def __init__(self, host, token):
        self._api_host = host
        self._api_token = token
    
    def url(self, *module, endpoint):
        if module:
            return f"{self._api_host}/api/{module}/{endpoint}"
        else:
            return f"{self._api_host}/api/{endpoint}"
    