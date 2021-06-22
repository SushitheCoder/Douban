import requests
import time

import logger
log = logger.LogModule()

class ReqWrapper:
    def __init__(self):
        if not hasattr(type(self), '_session'):
            self.creatSingletonSession()

    @classmethod
    def creatSingletonSession(cls):
        cls._session = requests.Session()

    def get(self, url, **kwargs):
        retry = 5
        while True:
            try:
                return self._session.get(url, **kwargs)
            except requests.ConnectionError as e:
                log.warning('Session get failed, retry:', retry)
                retry -= 1
                if retry < 1:
                    log.error("Retries end", e)
                    raise e
                time.sleep(2)

    def post(self, url, **kwargs):
        retry = 5
        while True:
            try:
                return self._session.post(url, **kwargs)
            except requests.ConnectionError as e:
                log.warning('Session post failed, retry:', retry)
                retry -= 1
                if retry < 1:
                    log.error("Retries end", e)
                    raise e
                time.sleep(2)
