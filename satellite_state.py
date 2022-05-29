import skyfield.sgp4lib as rv

satellite_param = []
AU_M = 149597870700  # per IAU 2012 Resolution B2
AU_KM = 149597870.700
DAY_S = 86400.0


def get_velocity(satellite, t):
    rTEME, vTEME, e = rv.EarthSatellite.ITRF_position_velocity_error(satellite, t)
    rTEME *= AU_KM
    vTEME *= AU_KM
    vTEME /= DAY_S
    return rTEME, vTEME


def set_satellite_param(t, rTEME, vTEME):
    t = str(t)
    rTEME = str(rTEME)
    vTEME = str(vTEME)
    satellite_param.append(t)
    satellite_param.append(rTEME)
    satellite_param.append(vTEME)


def get_satellite_param_string():
    return str(satellite_param)
