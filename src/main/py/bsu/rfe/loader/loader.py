from skyfield.api import load, wgs84
import configparser
import os
 
#@Kiryl
def loadTle():
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, 'main_config.properties')
    config = configparser.RawConfigParser()
    config.read(initfile)
    stations_url = config.get('DATABASE', 'database.tle.source.url')
    satellites = load.tle_file(stations_url)
    #for quantity print
    #print('Loaded', len(satellites), 'satellites')
    return satellites

