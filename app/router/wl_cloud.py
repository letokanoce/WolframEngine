import numpy as np

from fastapi import APIRouter
from typing import List
from wolframclient.serializers import export

from configuration.configs import Settings
from engine.wl_driver import WFConnector
from wolframscript.function import *


router = APIRouter()
settings = Settings()
wf_connector = WFConnector(settings)


@router.post("/calculate_mean")
def calculate_mean(mean: List[float], cov: List[List[float]], bounds: List[List[float]]):
    mean_wl = export(mean, target_format="wl").decode("utf-8")
    cov_wl = export(cov, target_format="wl").decode("utf-8")
    bounds_wl = export(np.array(bounds).T.tolist(),
                       target_format="wl").decode("utf-8")

    script = TRUNC_MULVAR_NORM + \
        "truncMultivarNorm[{}, {}, {}]".format(mean_wl, cov_wl, bounds_wl)
    result = wf_connector.run_script(script)

    return result.tolist()
