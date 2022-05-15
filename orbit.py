from numpy import array
from poliastro.twobody import Orbit
from astropy import time, units as u

from poliastro.bodies import Earth


def get_orbit(position:array, velocity:array, time_utc):
    orbit = Orbit.from_vectors(
        Earth,
        position * u.km,
        velocity * u.km / u.s,        
        #time_utc should be t.now()
        time.Time(time_utc.tai_strftime(format='%Y-%m-%d %H:%M'),scale="utc")
        
    )
    return orbit
