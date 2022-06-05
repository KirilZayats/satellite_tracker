from pytz import utc
import skyfield.sgp4lib as rv
from datetime import datetime
from skyfield.timelib import Time
from skyfield.api import wgs84,load
from db_proces import db_connection,get_sat
import satellite_loader

satellite_param = []
satellite_passes = []
AU_M = 149597870700  # per IAU 2012 Resolution B2
AU_KM = 149597870.700
DAY_S = 86400.0
altitude_degrees=10.0

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

def sattelite_passes_above_location(satellite:rv.EarthSatellite,topos,time_now: Time,days:Time)->tuple:
    return satellite.find_events(wgs84.latlon(topos[0],topos[1]),t0=time_now,t1=(time_now + days),altitude_degrees=altitude_degrees)

def get_satellite_param_string():
    return str(satellite_param)

def printMatrix ( matrix ): 
      for i in range ( len(matrix[1]) ): 
          print(((matrix[0][i]).utc_datetime()), "  ", ("start of signal reception" if matrix[1][i]==0 else ("end of signal reception" if matrix[1][i]==2 else "satellite culminated and started to descend again")))

def set_matrixToStr ( matrix ): 
    for i in range ( len(matrix[1]) ): 
       satellite_passes.append(str((matrix[0][i]).utc_datetime()) + "  " + ("start of signal reception" if matrix[1][i]==0 else ("end of signal reception" if matrix[1][i]==2 else "satellite culminated and started to descend again")))
      
def get_all_passese_satellites(topos,time_now):
    satellites_list = satellite_loader.get_satellitesList()

    passes_sat = " "
    con = db_connection();
    
    for satellite in satellites_list:
        date = time_now.date().getDate()
        time =time_now.time()
        ts = load.timescale()
        if len(sattelite_passes_above_location(satellite,topos,ts.from_datetime(datetime(date[0],date[1],date[2],time.hour(),time.minute(),tzinfo=utc)),0.0002)[0]) != 0:
            passes_sat = passes_sat + (get_sat(satellite.name,con))+'\n'
    return passes_sat



def get_sattelite_passes_above_location_string():
    strok = " "
    for i in range ( len(satellite_passes) ):
        strok = strok + satellite_passes[i] +'\n'
    return strok
   