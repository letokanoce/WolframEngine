from abc import ABC, abstractmethod

import numpy as np
from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession
from wolframclient.language import wlexpr

from app.configuration.configs import Settings


class WFConnection(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def run_script(self, script: str):
        pass


class WFConnector(WFConnection):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.session = self.create_session()

    def create_session(self):
        return WolframCloudSession(credentials=SecuredAuthenticationKey(self.settings.CONSUMER_KEY,
                                                                        self.settings.CONSUMER_PASSWORD))

    def run_script(self, script: str):
        self.session.start()
        result = self.session.evaluate(wlexpr(script))
        return np.array(result)
