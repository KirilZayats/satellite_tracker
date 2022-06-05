from requests import get
import os
import bs4 as bs
from dotenv import load_dotenv
import re


def get_country(sat_name:str):
    dotenv_path = os.path.join(os.path.dirname(__file__), 'pyth.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    doc_sdat = os.getenv('skyrocket_doc_sdat')
    sat_name1 = sat_name.lower().partition(' ')[0]
    regex = re.compile("\((.*)\)")
    sat_name2 = str(regex.findall(sat_name.lower()))
    response = get(str(doc_sdat + sat_name1 + ".htm"))
    if response.status_code == 404:
        sat_name1 = sat_name1.partition('-')[0]
        response = get(str(doc_sdat + sat_name1 + ".htm"))
        if response.status_code == 404:
            response = get(str(doc_sdat + sat_name2 + ".htm"))    
            if response.status_code == 404:
                sat_name2 = sat_name2.partition('-')[0]
                response = get(str(doc_sdat + sat_name2 + ".htm"))
                if response.status_code == 404:
                    response = get(str(doc_sdat + sat_name1+"_"+sat_name2 + ".htm"))
                    if response.status_code == 404:
                       return "Unknown";
    soup = bs.BeautifulSoup(str(response.content),'lxml')
    supa = soup.find('td',attrs={'id': 'sdnat'})
    country = supa.get_text();
    return country

