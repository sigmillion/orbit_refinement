# from skyfield.api import Topos
from skyfield.api import wgs84


class ground_site:
    def __init__(self, lat, lon):
        # Specify latitude and longitude in degrees
        # When specifying latitude, north is positive, south is negative
        # When specifying longitude, east is positive, west is negative
        # self.topos = Topos(lat, lon)
        self.topos = wgs84.latlon(lat, lon)
        return
