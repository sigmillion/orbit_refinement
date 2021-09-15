from skyfield.api import load, EarthSatellite
from sgp4.exporter import export_tle
from tle_utils import vec2tle, tle2vec
from random import uniform, randrange, seed


class satellite:
    def __init__(self, sat):
        self.sat = sat  # a link, not a copy of an EarthSatellite
        # self.vec = self.sat2vec()
        # self.line1, self.line2 = export_tle(sat.model)
        # self.Fc = 0  # Hertz [set this later]
        return

    def vec2sat(self, vec):
        line1, line2 = export_tle(self.sat.model)
        line1, line2 = vec2tle(vec, line1, line2)
        # print(line1)
        # print(line2)
        return EarthSatellite(line1, line2)

    def sat2vec(self):
        line1, line2 = export_tle(self.sat.model)
        # print(line1)
        # print(line2)
        return tle2vec(line1, line2)

    def perturb_satellite(self, scale=1.0):
        # Step 1. Extract vec
        # inclination, raan, ap, ma, mm = self.sat2vec()
        inclination, raan, ap, mm = self.sat2vec()

        # Step 2. Perturb the vec
        inclination = inclination + uniform(-1, 1) * scale
        self.inc_bounds = (inclination - scale, inclination + scale)
        
        raan = raan + uniform(-1, 1) * scale
        self.raan_bounds = (raan - scale, raan + scale)
        
        ap = ap + uniform(-1, 1) * scale
        self.ap_bounds = (ap - scale, ap + scale)
        
        # ma = ma + uniform(-1, 1) * scale
        # self.ma_bounds = (ma - scale, ma + scale)

        mm = mm + uniform(-1, 1) * scale * 0.1
        self.mm_bounds = (mm - scale*0.1, mm + scale*0.1)
        
        # minute = uniform(-1, 1) * scale
        # minute = minute / (24 * 60)
        # epoch_day = epoch_day + minute
        #vec = (inclination, raan, ap, ma, mm)
        vec = (inclination, raan, ap, mm)

        # Step 3. Return sat with perturbed vec
        return self.vec2sat(vec)

    def get_bounds(self):
        return [self.inc_bounds,
                self.raan_bounds,
                self.ap_bounds,
                self.mm_bounds]
        # return [self.inc_bounds,
        #         self.raan_bounds,
        #         self.ap_bounds,
        #         self.ma_bounds,
        #         self.mm_bounds]


class space:
    def __init__(self):
        self.load_satellites()
        return
    
    def load_satellites(self):
        # Download satellite TLEs
        stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
        self.satellites = load.tle_file(stations_url)  # returns list of EarthSatellite objects
        print('Load:', len(self.satellites), 'satellites')

        # Filter satellites by altitud at epoch
        range_lim = [350, 500]  # [km]
        range_mid = 0.5 * (range_lim[0] + range_lim[1])
        range_half = 0.5 * (range_lim[1] - range_lim[0])
        self.satellites = [s for s in self.satellites
                if abs(s.at(s.epoch).subpoint().elevation.km - range_mid) <= range_half]
        print('Filter:', len(self.satellites), 'satellites')
        return

    def select_satellite(self):
        # Select a satellite at random
        # i = randrange(0, len(self.satellites))
        i = 4
        print('Selected satellite index:', i, self.satellites[i].name)
        return self.satellites[i]
        # return self.satellites[4]

