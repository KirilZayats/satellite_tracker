from skyfield.api import load

import loader


def main():
    satellites = loader.loadTle()
    by_name = {sat.name: sat for sat in satellites}
    # Just tle example
    satellite = by_name['ISS (ZARYA)']
    print(satellite)
    ts = load.timescale()
    t = ts.now()


if __name__ == "__main__":
    main()
