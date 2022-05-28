from numpy import (
    array, multiply, ndarray
)
from skyfield.positionlib import ICRF
import array
import math

import skyfield.sgp4lib as rv

AU_M = 149597870700  # per IAU 2012 Resolution B2
AU_KM = 149597870.700
DAY_S = 86400.0


def get_velocity(satellite, t):
    rTEME, vTEME, e = rv.EarthSatellite.ITRF_position_velocity_error(satellite, t)
    rTEME *= AU_KM
    vTEME *= AU_KM
    vTEME /= DAY_S
    return rTEME, vTEME


def print_in_file_state(t, satellite, rTEME, vTEME):
    satellite_param = [t, satellite, rTEME, vTEME]
    with open(r"ui\satellite_state.txt", "w") as file:
        for line in satellite_param:
            file.write(line + '\n')


def get_satellite_info_file():
    satellite_param = []
    with open(r"ui\satellite_state.txt", "r") as file:
        for line in satellite_param:
            satellite_param = file.read(line + '\n')
    return satellite_param
