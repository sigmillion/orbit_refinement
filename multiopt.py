from satellite_utils import space, satellite
from ground_site import ground_site
from link import link
from scipy.optimize import minimize
import numpy as np

def objective(x, links_est, links_true, prediction=False):
    new_sat = satellite(links_est[0].sat.vec2sat(x))
    for le in links_est:
        le.sat = new_sat

    # Select overpasses for estimated links
    total_error = 0.0
    total_samples = 0
    prediction_error = 0.0
    prediction_samples = 0
    for le, lt in zip(links_est, links_true):
        le.copy_overpasses(lt.overpass_times_list)
        le.compute_range_tables()
        new_error, new_samples, new_prediction_error, new_prediction_samples = lt.compute_range_rate_error(le)
        total_error = total_error + new_error
        total_samples = total_samples + new_samples
        prediction_error = prediction_error + new_prediction_error
        prediction_samples = prediction_samples + new_prediction_samples
    print('Range rate error = ', total_error / total_samples)
    if prediction==False:
        return total_error / total_samples
    else:
        return prediction_error / prediction_samples

def runopt(num_ground_sites=3, window_length_days=3, num_overpasses=3):
    # Get a satellite
    leo = space()
    sat_true = satellite(leo.select_satellite())
    # sat_true = satellite(sat_true.vec2sat(sat_true.sat2vec()))  # is this just for testing???

    # Get a perturbed TLE satellite
    sat_est = satellite(sat_true.perturb_satellite(0.1))
    # sat_est = sat_true
    perturb_box = sat_true.get_bounds()
    
    # Get a list of ground sites
    ground_sites = []
    for i in range(num_ground_sites):
        ground_sites.append(ground_site(0.0,10.0*i))  # Put ground sites around equator

    # Setup ground-satellite links
    links_true = [link(gs, sat_true, window_length_days, num_overpasses) for gs in ground_sites]
    links_est  = [link(gs, sat_est,  window_length_days, num_overpasses) for gs in ground_sites]

    # Select overpasses for estimated links
    total_error = 0.0
    total_samples = 0
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
        total_error = total_error + new_error
        total_samples = total_samples + new_samples
    print('Range rate error = ', total_error / total_samples)

    # Test code
    # x0 = sat_est.sat2vec()
    # x0 = sat_true.sat2vec()
    # print(x0)
    # val = objective(x0, links_est, links_true)
    # print(val)
    # return
    
    # 4. Use Nelder-Mead to minimize this objective.
    xt = sat_true.sat2vec()
    xe = sat_est.sat2vec()
    opt_result = minimize(objective, xe,
                        args=(links_est, links_true),
                        method='Nelder-Mead',
                        bounds=perturb_box,
                        options={'xatol' : 1e-10, 'fatol' : 1e-10})

    xe = np.array(xe)
    xt = np.array(xt)
    xo = opt_result.x
    fo = opt_result.fun
    nit = opt_result.nit
    print(xe)
    print(xt)
    print(xo)
    print(fo)
    print(nit)
    print(opt_result.message)
    fp = objective(xo, links_est, links_true, prediction=True)
    
    # We want to find out how many ground sites and overpasses
    # lead to an identifiable solution.

    # Ask Charles what TLE parameters are the most vital for
    # overpass estimation and why.  Take better notes this
    # time.
    
    return xt, xe, xo, fo, fp, nit


if __name__ == "__main__":
    # execute only if run as a script
    runopt(num_ground_sites=1, window_length_days=3, num_overpasses=1)
