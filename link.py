from skyfield.api import load, EarthSatellite
from sgp4.exporter import export_tle
from time_utils import overpass_times, tt2min, hour2tt, tt2sec, sec2tt
import numpy as np
# from skyfield.framelib import itrs


class link:
    def __init__(self, ground_site, satellite):
        self.gnd = ground_site
        self.sat = satellite
        self.overpass_times_list = []
        self.ranges = []
        self.range_rates = []
        self.min_altitude_degrees = 20
        self.window_length_days = 3
        self.number_overpasses = 3
        return
    
    def select_overpasses(self):
        ts = load.timescale()
        t0 = self.sat.sat.epoch
        t1 = ts.tt_jd(t0.tt + self.window_length_days)
        tm, ev = self.sat.sat.find_events(self.gnd.topos, t0, t1, altitude_degrees=self.min_altitude_degrees)
        # Make a list of rise and set times
        rise_set = [(t.tt, e, i)
                        for t, e, i in zip(tm, ev, range(len(tm)))
                        if e in [0, 2]]  # 0 = overpass rise, 2 = overpass set

        # Make a list of overpass durations
        duration = [(tt2min(rise_set[i][0] - rise_set[i - 1][0]), rise_set[i - 1][2], rise_set[i][2])
                        for i in range(len(rise_set)) if rise_set[i][1] == 2]  # 2 = overpass set time
        # Sort list of durations
        duration.sort(key=lambda x: x[0])
        # Select the longest overpasses
        duration = duration[-self.number_overpasses:]
        # Process each remaining overpass
        for d in duration:
            ot = overpass_times(tm[d[1]].tt, tm[d[2]].tt)
            self.overpass_times_list.append(ot)
            # print('(Lat,Lon) = (', self.gnd.topos.latitude, ',', self.gnd.topos.longitude, ')')
            print('Overpass duration [min] = ', tt2min(ot.end_time - ot.begin_time))
        return

    def copy_overpasses(self, overpass_times_list):
        self.overpass_times_list = []
        for ot in overpass_times_list:
            ot_new = overpass_times(ot.begin_time, ot.end_time)
            self.overpass_times_list.append(ot_new)
        return

    def find_matching_overpasses(self, overpass_times_list):
        ts = load.timescale()
        self.overpass_times_list = []
        for ot in overpass_times_list:
            t0 = ts.tt_jd(ot.begin_time - hour2tt(0.5))  # back 30 minutes
            t1 = ts.tt_jd(ot.end_time + hour2tt(0.5))  # forward 30 minutes
            tm, ev = self.sat.sat.find_events(self.gnd.topos, t0, t1, altitude_degrees=self.min_altitude_degrees)
            #print('Found', len(tm) / 3, 'events')  # Should find only one
            if len(tm) > 3 or len(tm) == 0:
                print('ERROR: Should find exactly one matching events.')
            ot_new = overpass_times(tm[0].tt, tm[2].tt)
            self.overpass_times_list.append(ot_new)
            print('Time diff start = ',tt2sec(ot_new.begin_time - ot.begin_time))
            print('Time diff end   = ',tt2sec(ot_new.end_time - ot.end_time))
        return

    def compute_range_tables(self):
        ts = load.timescale()
        difference = self.sat.sat - self.gnd.topos
        #times = []
        #real_times = []
        self.ranges = []
        self.range_rates = []
        for ot in self.overpass_times_list:
            t = ot.sample_times
            rt = ts.tt_jd(ot.begin_time + sec2tt(t))
            dt = difference.at(rt)
            r = [np.linalg.norm(d.position.km) for d in dt]

            rt1 = ts.tt_jd(ot.begin_time + sec2tt(t + 1.0))
            rt0 = ts.tt_jd(ot.begin_time + sec2tt(t - 1.0))
            dt1 = difference.at(rt1)
            dt0 = difference.at(rt0)
            rr = np.zeros((len(r),))
            for i in range(len(r)):
                rr[i] = dt1[i].distance().km - dt0[i].distance().km
            self.ranges.append(np.array(r))
            self.range_rates.append(rr)
        return

    def compute_range_rate_error(self, other_link):
        total_error = 0.0
        for rr0, rr1 in zip(self.range_rates, other_link.range_rates):
            total_error = total_error + np.linalg.norm(rr0 - rr1)
        return total_error
