# Useful for defining quantities
from astropy import units as u

from poliastro.twobody import Orbit

# Earth focused modules, ISS example orbit and time span generator
from poliastro.earth import EarthSatellite
from poliastro.earth.plotting import GroundtrackPlotter
from poliastro.util import time_range


def get_orbit_plot(orbit:Orbit):
    # Build spacecraft instance
    satellite_spacecraft = EarthSatellite(orbit, None)
    t_span = time_range(start = orbit.epoch - 1.5 * u.h, periods=150, end = orbit.epoch + 1.5 * u.h)
    # Generate an instance of the plotter, add title and show latlon grid
    gp = GroundtrackPlotter()
    gp.update_layout(title="International Space Station groundtrack")

    # Plot previously defined EarthSatellite object
    gp.plot(
        satellite_spacecraft,
        t_span,
        label="Satellite",
        color="red",
        marker={"size": 10, "symbol": "triangle-right", "line": {"width": 1, "color": "black"}},
    )
    # For building geo traces
    import plotly.graph_objects as go

    # Faculty of Radiophysics and Computer Technologies coordinates
    STATION = [53.83821551524637, 27.476136409973797] * u.deg

    # Let us add a new trace in original figure
    gp.add_trace(
        go.Scattergeo(
            lat=STATION[0],
            lon=STATION[-1],
            name="Faculty of Radiophysics and Computer Technologies",
            marker={"color": "blue"},
        )
    )
    gp.fig.show()
    # Switch to three dimensional representation
    gp.update_geos(projection_type="orthographic")
    gp.fig.show()

