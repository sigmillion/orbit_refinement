from satellite_utils import space, satellite
from ground_site import ground_site
from link import link


def main():
    # Get a satellite
    leo = space()
    sat_true = satellite(leo.select_satellite())
    # sat_true = satellite(sat_true.vec2sat(sat_true.sat2vec()))  # is this just for testing???

    # Get a perturbed TLE satellite
    sat_est = satellite(sat_true.perturb_satellite(0.1))
    # sat_est = sat_true
    
    # Get a list of ground sites
    ground_sites = [ground_site(0.0, 0.0),
                    ground_site(10.0, 10.0),
                    ground_site(20.0, 20.0)]

    # Setup ground-satellite links
    links_true = [link(gs, sat_true) for gs in ground_sites]
    links_est  = [link(gs, sat_est ) for gs in ground_sites]

    # Select overpasses for estimated links
    total_error = 0.0
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
        total_error = total_error + lt.compute_range_rate_error(le)
    print('Range rate error = ', total_error)

    # 4. Use Nelder-Mead to minimize this objective.

    # We want to find out how many ground sites and overpasses
    # lead to an identifiable solution.

    # Ask Charles what TLE parameters are the most vital for
    # overpass estimation and why.  Take better notes this
    # time.

    
    
    return


if __name__ == "__main__":
    # execute only if run as a script
    main()
