from numpy import (
    array, multiply, ndarray
)
from skyfield.positionlib import ICRF
import array
import math

import skyfield.sgp4lib as rv

AU_M = 149597870700             # per IAU 2012 Resolution B2
AU_KM = 149597870.700
DAY_S = 86400.0

def get_velocity(satellite,t):
    rTEME, vTEME, e = rv.EarthSatellite.ITRF_position_velocity_error(satellite,t)
    rTEME *= AU_KM
    vTEME *= AU_KM
    vTEME /= DAY_S
    return rTEME,vTEME