from skyfield.api import load

import satellite_state
from satellite_state import get_velocity
import loader
import orbit
import orbit_plot


def main_default():
    satellites = loader.loadTle()
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['KITSUNE']
    ts = load.timescale()
    t = ts.now()
    print(t)
    print(satellite)
    rTEME, vTEME = get_velocity(satellite, t)
    print(rTEME, vTEME)
    satellite_state.set_satellite_param(t, rTEME, vTEME)
    orbit_vl = orbit.get_orbit(rTEME, vTEME, t)
    orbit_plot.get_orbit_plot(orbit_vl)


def main_another(satellites, satellite_name):
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name[satellite_name]
    ts = load.timescale()
    t = ts.now()
    print(t)
    print(satellite)
    rTEME, vTEME = get_velocity(satellite, t);
    print(rTEME, vTEME)
    orbit_vl = orbit.get_orbit(rTEME, vTEME, t)
    orbit_plot.get_orbit_plot(orbit_vl)


if __name__ == "__main__":
    main_default()
