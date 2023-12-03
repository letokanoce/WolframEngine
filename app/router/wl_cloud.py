from fastapi import APIRouter
from wolframclient.serializers import export

from app.configuration.configs import Settings
from app.engine.wl_driver import WFConnector
from app.wolframscript.function import *

router = APIRouter()
settings = Settings()
wf_connector = WFConnector(settings)


@router.post("/calculate/truncated/dist")
def calculate_mean(mean: list, cov: list, bounds: list):
    mean_wl = export(mean, target_format="wl").decode("utf-8")
    cov_wl = export(cov, target_format="wl").decode("utf-8")
    bounds_wl = export(bounds, target_format="wl").decode("utf-8")
    script = TRUNC_MULVAR_NORM + "truncMultivarNorm[{}, {}, {}]".format(mean_wl, cov_wl, bounds_wl)
    result = wf_connector.run_script(script)
    wf_connector.session.stop()
    return result.tolist()


@router.get("/calculate/generated/p_val")
def calculate_mean(dim: int):
    script = GENERATE_CARTESIAN_PVAL + "generateCartesianPval[{}]".format(dim)
    result = wf_connector.run_script(script)
    wf_connector.session.stop()
    return result.tolist()


@router.post("/calculate/optimized/cov")
def calculate_optimized_cov(cov_mtx_co: list, cov_mtx_sd_pro: list):
    cov_mtx_elems_wl = export(cov_mtx_co, target_format="wl").decode("utf-8")
    cov_mtx_sd_pro_wl = export(cov_mtx_sd_pro, target_format="wl").decode("utf-8")
    script = GENERATE_CARTESIAN_PVAL + "optimizedCovMatrix[{},{}]".format(cov_mtx_elems_wl, cov_mtx_sd_pro_wl)
    result = wf_connector.run_script(script)
    wf_connector.session.stop()
    return result.tolist()
