import numpy as np
from abc import ABC, abstractmethod
from configuration.configs import Settings
from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession
from wolframclient.language import wlexpr


class WFConnection(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def run_script(self):
        pass


class WFConnector(WFConnection):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.session = self.create_session()

    def create_session(self):
        return WolframCloudSession(credentials=SecuredAuthenticationKey(self.settings.COSUMER_KEY,
                                                                        self.settings.COSUMER_PASSWORD))

    def run_script(self, script: str):
        result = self.session.evaluate(wlexpr(script))
        return np.array(result)
