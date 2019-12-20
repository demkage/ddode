from typing import List
import random

class ProxyEntry:
    def __init__(self, host: str, port: int, headers: dict):
        self.host = host
        self.port = port
        self.headers = headers

class ProxySelector:
    def __init__(self, proxies: List[ProxyEntry]):
        self.proxies = proxies

    def select(self) -> ProxyEntry:
        return self.proxies[0]

class RandProxySelector(ProxySelector):
    def __init__(self, proxies: List[ProxyEntry]):
        ProxySelector.__init__(self, proxies)
    
    def select(self) -> ProxyEntry:
        proxy = self.proxies[random.randrange(len(self.proxies))]
        return proxy
