from skyfield.api import load
from satellite_state import get_velocity
import loader
import orbit
import orbit_plot

def main():
    satellites = loader.loadTle()
    by_name = {sat.name: sat for sat in satellites}
    # Just tle example
    satellite = by_name['KITSUNE']
    ts = load.timescale()
    t = ts.now();
    print(t)
    print(satellite)
    rTEME,vTEME = get_velocity(satellite,t);
    print(rTEME,vTEME)
    orbit_vl = orbit.get_orbit(rTEME,vTEME,t)
    orbit_plot.get_orbit_plot(orbit_vl)


if __name__ == "__main__":
    main()
