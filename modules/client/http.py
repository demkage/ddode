from modules.client.proxy import ProxyEntry
from http.client import HTTPSConnection
from http.client import HTTPResponse

class HTTPRules:
    def __init__(self, properties: dict):
        self.accept_cookies = properties.setdefault('accept_cookies', False)
        self.reject_cookies_after = properties.setdefault('reject_cookies_after', -1)
    
    def __str__(self):
        return f"accept_cookies: {self.accept_cookies}, reject_cookies_after: {self.reject_cookies_after}"

class HTTPClientConfiguration:
    def __init__(self, properties: dict):
        self.host = properties['host']
        self.port = properties.setdefault('port', 443)
        self.rules = HTTPRules(properties.setdefault('rules', dict()))
    
    def __str__(self):
        return f"host: {self.host}, port: {self.port}, rules: [{self.rules}]"

class HTTPClientResonse:
    def __init__(self, response: HTTPResponse):
        self.response = response
        self.body = response.read()
        self.status_code = self.response.code
        self.headers = self.response.headers

class HTTPClient:
    def __init__(self, configuration: HTTPClientConfiguration, proxy: ProxyEntry = None, headers: dict = dict()):
        self.configuration = configuration
        self.proxy = proxy
        self.default_headers = headers
        self.local_store = dict()
    
    def request(self, method: str, endpoint: str, body = None, headers: dict = dict()) -> HTTPClientResonse:
        self.__pre_request_process__(method, endpoint, headers)
        request_headers = self.__resolve_headers__(headers)

        connection = HTTPSConnection(self.configuration.host, self.configuration.port)
        if self.proxy is not None:
            connection.set_tunnel(self.proxy.host, self.proxy.port, self.proxy.headers)

        connection.putheader
        connection.request(method, endpoint, body, headers=request_headers)
        response  = HTTPClientResonse(connection.getresponse())
        connection.close()
        self.__post_response_process__(response)
        return response

    def __pre_request_process__(self, method: str, endpoint: str, headers: dict):
        if self.configuration.rules.reject_cookies_after != -1 and self.configuration.rules.accept_cookies:
            used_cookies_times = self.local_store['used_cookies_times'] if 'used_cookies_times' in self.local_store else 0
            if used_cookies_times >= self.configuration.rules.reject_cookies_after:
                self.local_store['cookies'] = ""

    def __resolve_headers__(self, additional_headers: dict) -> dict:
        result_headers = dict(self.default_headers)
        result_headers.update(additional_headers)

        if 'cookies' in self.local_store:
            result_headers['cookies'] = self.local_store['cookies']

        return result_headers
    
    def __post_response_process__(self, response: HTTPClientResonse):
        if self.configuration.rules.accept_cookies:
            if 'set-cookie' in response.headers:
                cookies = response.headers['set-cookie']
                self.local_store['cookies'] = cookies
                self.local_store['used_cookies_times'] = 0
            elif 'cookies' in self.local_store and self.local_store['cookies'] is not "":
                current_used_times = self.local_store['used_cookies_times'] if 'used_cookies_times' in self.local_store else 0
                self.local_store['used_cookies_times'] = current_used_times + 1
