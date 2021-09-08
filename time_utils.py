import numpy as np

def tt2hour(val: float) -> float:
    return val * 24.0  # hours per day


def hour2tt(val: float) -> float:
    return val / 24.0  # hours per day


def tt2min(val: float) -> float:
    return val * 1440.0  # minutes per day


def min2tt(val: float) -> float:
    return val / 1440.0  # minutes per day


def tt2sec(val: float) -> float:
    return val * 86400.0  # seconds/day


def sec2tt(val: float) -> float:
    return val / 86400.0  # seconds/day


class overpass_times:
    def __init__(self, begin: float, end: float):
        self.begin_time = begin
        self.end_time = end
        self.sample_time_seconds = 10  # Sample every 10 seconds
        self.sample_rate_hertz = 1.0 / self.sample_time_seconds
        self.sample_times = None
        return

    def get_duration_seconds(self):
        return tt2sec(self.end_time - self.begin_time)

    def make_time_array(self):
        num_seconds = tt2sec(self.end_time - self.begin_time)
        num_samples = int(num_seconds * self.sample_rate_hertz)
        self.sample_times = np.arange(0.0, num_samples) * self.sample_time_seconds
        return

    def link_sample_times(self, ot):
        self.begin_time = ot.begin_time
        self.end_time = ot.end_time
        self.sample_times = ot.sample_times
        return
