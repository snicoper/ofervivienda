import json

from django.conf import settings

import googlemaps
import requests


class Location2Address(object):
    """Obtener dirección formateada y latitude longitude de una dirección.

    Pasando un address de un usuario, se obtiene la lat y long además
    de obtener las partes de una dirección.

    Nota: Actualmente no se usa en ningún sitio, pero lo dejo para el futuro.
    """
    gmaps = googlemaps.Client(key=settings.GMAPS_APIKEY_PYTHON)

    def __init__(self, address):
        geocode_result = self.gmaps.geocode(address, language='en')
        geometry = geocode_result[0]['geometry']
        self.address_components = geocode_result[0]['address_components']
        self.formatted_address = geocode_result[0]['formatted_address']
        self.latitude = geometry['location']['lat']
        self.longitude = geometry['location']['lng']
        self.country = None
        self.state = None
        self.city = None
        self.address = None
        self.zipcode = 0
        self.street_number = 0
        for component_type in self.address_components:
            if 'country' in component_type['types']:
                self.country = component_type['long_name']
            if 'administrative_area_level_2' in component_type['types']:
                self.state = component_type['long_name']
            if 'locality' in component_type['types']:
                self.city = component_type['long_name']
            if 'route' in component_type['types']:
                self.address = component_type['long_name']
            if 'postal_code' in component_type['types']:
                self.zipcode = component_type['long_name']
            if 'street_number' in component_type['types']:
                self.street_number = component_type['long_name']


def user_ip_info(user_ip, as_json=True):
    """Obtener información geográfica con una ip.

    Los datos pueden ser aproximados.

    Estos son los campos obtenidos.
        - country_name
        - city
        - region_code
        - time_zone
        - longitude
        - latitude
        - metro_code
        - country_code
        - zip_code
        - ip
        - region_name

    @ver: http://freegeoip.net/

    "You're allowed up to 15,000 queries per hour by default. Once this limit is
    reached, all of your requests will result in HTTP 403, forbidden, until your
    quota is cleared."

    Args:
        user_ip (str): Ip de la que obtener información.
        as_json (bool): Convertir los datos en json? de lo contrario en Python.

    Returns:
        dict|json: Diccionario con las claves puestas en la descripción (Python).
        Si se le pasa as_json=False, se obtiene el valor en json (javascript)
    """
    try:
        url = 'http://freegeoip.net/json/{}'.format(user_ip)
        response = requests.get(url)
        if as_json:
            return response.text
        return json.loads(response.text)
    except:
        return None
