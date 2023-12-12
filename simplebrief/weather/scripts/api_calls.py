import requests
import re
from simplebrief.local_settings import *

def get_metar(icao_code) :
    url = f'https://aviationweather.gov/api/data/metar?ids={icao_code}'
    
    try :
        response = requests.get(url, timeout = 5)
        metar = response.text

        return metar
    
    except requests.exceptions.HTTPError as e :
        error = (f'An HTTP error has occured: {e}')

        return error
        

def get_taf(icao_code) :
    url = f'https://aviationweather.gov/cgi-bin/data/taf.php?ids={icao_code}'
    
    try :
        response = requests.get(url, timeout = 5)
        taf = response.text
        split_taf = taf.split('\n')

        return taf
        
    except requests.exceptions.HTTPError as e :
        error = (f'An HTTP error has occured: {e}')

        return error


#USES FAA NOTAM API
def get_notams(icao_code) :
    version = 'v1'
    url = f'https://external-api.faa.gov/notamapi/{version}'

    headers = {
        'client_id' : faa_client_id,
        'client_secret' : faa_api_key,
    }

    params = {
        'icaoLocation' : icao_code,
        'responseFormat' : 'aixm',
        
    }

    try :
        response = requests.get(url, headers=headers, params=params)
        notams = response.text

        
        print(notams)

        return notams

    except requests.exceptions.HTTPError as e :
        error = (f'An HTTP error has occured: {e}')

        return error