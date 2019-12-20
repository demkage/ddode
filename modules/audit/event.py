from enum import Enum
import time
from http.client import HTTPResponse

class EventType(Enum):
    REQUEST = 1
    RESPONSE = 2
    PROXY = 3

class Event:
    def __init__(self, type: EventType, timestamp: int):
        self.type = type
        self.timestamp = timestamp
    
    def is_request_type(self) -> bool:
        return self.type == EventType.REQUEST
    
    def is_response_type(self) -> bool:
        return self.type == EventType.RESPONSE

    def is_proxy_type(self) -> bool:
        return self.type == EventType.PROXY
    
    def get_event_timestamp(self) -> int:
        return self.timestamp

class RequestEvent(Event):
    def __init__(self, method: str, uri: str, proxy: str):
        Event.__init__(self, EventType.REQUEST, time.time())
        self.method = method
        self.uri = uri
        self.proxy = proxy
    
    def get_method(self) -> str:
        return self.method

    def is_method(self, expected_type: str) -> bool:
        return self.method == expected_type
    
    def get_uri(self) -> str:
        return self.uri

    def is_using_proxy(self) -> bool: 
        return self.proxy != None
    
    def get_proxy(self) -> str:
        return self.proxy

class ResponseEvent(Event):
    def __init__(self, source: RequestEvent, response: HTTPResponse):
        Event.__init__(self, EventType.RESPONSE, time.time())
        self.source = source
        self.response = response
    
    def get_source_event(self) -> RequestEvent:
        return self.source
    
    def get_request_start_timestamp(self) -> int:
        return self.source.get_event_timestamp()
    
    def get_request_end_timestamp(self) -> int:
        return self.get_event_timestamp()
    
    def get_execution_time_in_s(self) -> int:
        start = self.get_request_start_timestamp()
        end = self.get_request_end_timestamp()
        return end - start
    
    def get_reponse(self) -> HTTPResponse:
        return self.response
    
    def is_failed(self) -> bool:
        return self.response.status >= 400
    
    def is_server_error(self) -> bool:
        return self.response.status >= 500

    def is_client_error(self) -> bool:
        return self.response.status < 500 and self.response.status >= 400
    
class ProxyEvent(Event):
    def __init__(self, host: str, failed: bool):
        Event.__init__(self, EventType.PROXY, time.time())
        self.host = host
        self.failed = failed
    
    def get_host(self):
        return self.host
    
    def is_failed(self):
        return self.failed