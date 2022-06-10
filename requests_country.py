from requests import get
import os
import bs4 as bs
from dotenv import load_dotenv


def get_country(satnum:str):
    dotenv_path = os.path.join(os.path.dirname(__file__), 'pyth.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    n2yo_sdat = os.getenv('n2yo_doc_sdat')
    response1 = get(n2yo_sdat+str(satnum))
    if response1.status_code == 404:
        return 'Unknown'
    soup1 = bs.BeautifulSoup(str(response1.content),'lxml')
    supa1 = soup1.find(name='div',attrs={'id': 'satinfo'})
    #print(supa1)
    return (str(supa1).split('<b>Source</b>:')[1]).split('<br/><b>Launch')[0].split(')')[0] + ')';