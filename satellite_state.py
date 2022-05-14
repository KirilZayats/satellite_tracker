
def get_position(satellite, time_utc):
    geocentric = satellite.at(time_utc)
    return geocentric.position.km

# def get_velocity(satellite):
#     velocity =
#     return velocity