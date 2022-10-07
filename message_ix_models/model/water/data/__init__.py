"""Generate input data."""

import logging

from message_ix_models import ScenarioInfo
from message_ix_models.util import add_par_data
from .infrastructure import add_infrastructure_techs
from .water_for_ppl import cool_tech, non_cooling_tec
from .demands import add_sectoral_demands, add_water_availability, add_irrigation_demand
from .infrastructure import add_infrastructure_techs, add_desalination
from .water_supply import add_water_supply, add_e_flow
from .irrigation import add_irr_structure

log = logging.getLogger(__name__)

DATA_FUNCTIONS = [
    add_water_supply,
    cool_tech,  # Water & parasitic_electricity requirements for cooling technologies
    non_cooling_tec,
    add_sectoral_demands,
    add_water_availability,
    add_irrigation_demand,
    add_infrastructure_techs,
    add_desalination,
    add_e_flow,
    add_irr_structure,
]

DATA_FUNCTIONS_COUNTRY = [
    add_water_supply,
    cool_tech,  # Water & parasitic_electricity requirements for cooling technologies
    non_cooling_tec,
    add_sectoral_demands,
    add_water_availability,
    add_irrigation_demand,
    add_infrastructure_techs,
    add_desalination,
    add_e_flow,
]


def add_data(scenario, context, dry_run=False):
    """Populate `scenario` with MESSAGEix-Nexus data."""

    info = ScenarioInfo(scenario)
    context["water build info"] = info

    data_funcs = (
        [add_water_supply, cool_tech, non_cooling_tec]
        if context.nexus_set == "cooling"
        else DATA_FUNCTIONS
        if context.type_reg == "global"
        else DATA_FUNCTIONS_COUNTRY
    )

    for func in data_funcs:
        # Generate or load the data; add to the Scenario
        log.info(f"from {func.__name__}()")
        add_par_data(scenario, func(context), dry_run=dry_run)

    log.info("done")
