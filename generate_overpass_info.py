from satellite_utils import space, satellite
from ground_site import ground_site
from link import link
from scipy.optimize import minimize
import numpy as np

def generate(num_ground_sites=1, window_length_days=3, num_overpasses=1):
    # Get a satellite
    leo = space()
    sat_true = satellite(leo.select_satellite())

    # Get a perturbed TLE satellite
    sat_est = satellite(sat_true.perturb_satellite(1.0))  # One degree of perturbation
    perturb_box = sat_true.get_bounds()
    
    # Get a list of ground sites
    ground_sites = []
    for i in range(num_ground_sites):
        ground_sites.append(ground_site(0.0,10.0*i))  # Put ground sites around equator

    # Setup ground-satellite links
    links_true = [link(gs, sat_true, window_length_days, num_overpasses) for gs in ground_sites]
    links_est  = [link(gs, sat_est,  window_length_days, num_overpasses) for gs in ground_sites]

    # Select overpasses for estimated links
    for le, lt in zip(links_est, links_true):
        le.select_overpasses()
        lt.copy_overpasses(le.overpass_times_list)
        # Set up the sample time arrays
        for ote, ott in zip(le.overpass_times_list, lt.overpass_times_list):
            ote.make_time_array()
            ott.make_time_array()
        # Compute the range tables
        lt.compute_range_tables()
        le.compute_range_tables()
        new_error, new_samples, predict_error, predict_samples = lt.compute_range_rate_error(le)

    return

if __name__ == "__main__":
    # execute only if run as a script
    generate(num_ground_sites=1, window_length_days=3, num_overpasses=1)
