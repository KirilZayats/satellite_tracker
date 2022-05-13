from skyfield.api import load
from dotenv import load_dotenv
import os
 
#@Kiryl
def loadTle():
    dotenv_path = os.path.join(os.path.dirname(__file__), 'pyth.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    stations_url = os.getenv('tle_source_url')
    satellites = load.tle_file(stations_url)
    #for quantity print
    #print('Loaded', len(satellites), 'satellites')
    return satellites