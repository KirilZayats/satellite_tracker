from skyfield.api import load

import satellite_state
from satellite_state import get_velocity,sattelite_passes_above_location
import loader
import orbit
import orbit_plot



_selected_sat = "CUBEBUG-2 (LO-74)"

@staticmethod
def set_selected_sat(new_name: str):
    _selected_sat = new_name


@staticmethod
def get_satellitesList():
    return loader.loadTle();

def main_default():
    satellites = get_satellitesList()
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name[_selected_sat]
    ts = load.timescale()
    t = ts.now()
    print(t)
    print(satellite)
    rTEME, vTEME = get_velocity(satellite, t)
    print(rTEME, vTEME)
    STATION = [53.83821551524637, 27.476136409973797] 
    satellite_state.set_satellite_param(t, rTEME, vTEME)
    satellite_state.set_matrixToStr(sattelite_passes_above_location(satellite,STATION,t))
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
