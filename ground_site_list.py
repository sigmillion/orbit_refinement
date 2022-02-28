from ground_site import ground_site

class gse:
    def __init__(self, lat, lon, name):
        self.ground_site = ground_site(lat, lon)
        self.name = name

ground_site_list = [gse(21.2788, -157.8336, 'Hawaii'),
                    gse(13.44, 144.66, 'Guam'),
                    gse(18.0069, -66.5000, 'Puerto Rico'),
                    gse(26.7, 128.25, 'Okinawa'),
                    gse(1.366667, 103.8, 'Singapore'),
                    gse(38.761667, -27.095, 'Azores'),
                    gse(8.716667, 167.733333, 'Kwajalein Island'),
                    gse(-7.933333, -14.416667, 'Ascension Island'),
                    gse(-7.319500, 72.422859, 'Diego Garcia')]


