from satellite_utils import space, satellite
from multiopt import runopt
import numpy as np
import random


if __name__ == "__main__":
    # Set the seed for repeatability
    seed_val = 1234
    random.seed(seed_val)

    # Get a satellite
    leo = space()
    sat_true = satellite(leo.select_satellite())

    # Set simulation parameters
    num_overpasses = [1, 3, 5]
    num_groundsites = [1, 3, 5]
    num_iterations = 1
        
    # Save data
    with open('data.npy', 'wb') as f:
        np.save(f, np.array([seed_val]))
        np.save(f, np.array(num_overpasses))
        np.save(f, np.array(num_groundsites))
        np.save(f, np.array([num_iterations]))

        for k in range(num_iterations):
            # Get a perturbed TLE satellite
            sat_est = satellite(sat_true.perturb_satellite(0.1))
            # vals = sat_true.sat2vec()
            # print(vals)
            # vals = sat_est.sat2vec()
            # print(vals)
            # continue

            for ng in range(len(num_groundsites)):
                for no in range(len(num_overpasses)):
                    xt, xe, xo, fo, fp, nit = runopt(sat_true, sat_est,
                                                    num_groundsites[ng],
                                                    num_overpasses[no],
                                                    num_overpasses[no])
                    np.save(f, np.array([num_groundsites[ng], num_overpasses[no], k, fo, fp, nit]))
                    np.save(f, xt)
                    np.save(f, xe)
                    np.save(f, xo)

    

