from multiopt import runopt
import numpy as np
import random


if __name__ == "__main__":
    seed_val = 1234
    random.seed(seed_val)  # Set the seed for repeatability
    num_overpasses = [1, 3, 5, 7]
    num_groundsites = [1, 3, 5, 7]
    num_iterations = 30

    # Save data
    with open('data.npy', 'wb') as f:
        np.save(f, np.array([seed_val]))
        np.save(f, np.array(num_overpasses))
        np.save(f, np.array(num_groundsites))
        np.save(f, np.array([num_iterations]))

        for no in range(len(num_overpasses)):
            for ng in range(len(num_groundsites)):
                for k in range(num_iterations):
                    xt, xe, xo, fo, nit = runopt(num_groundsites[ng],
                                                    num_overpasses[no],
                                                    num_overpasses[no])
                    np.save(f, np.array([num_groundsites[ng], num_overpasses[no], k, fo, nit]))
                    np.save(f, xt)
                    np.save(f, xe)
                    np.save(f, xo)

    
