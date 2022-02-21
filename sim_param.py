# Set simulation parameters
import numpy as np

# Set simulation parameters
num_overpasses = [1, 3, 5]
num_groundsites = [1, 3]
num_iterations = 4

fovals = np.ndarray((num_iterations,len(num_groundsites),len(num_overpasses)))
fpvals = np.ndarray((num_iterations,len(num_groundsites),len(num_overpasses)))
xerr = np.ndarray((num_iterations,len(num_groundsites),len(num_overpasses)))

with open('data.npy', 'rb') as f:
    seed_val = np.load(f)
    seedd_val = seed_val[0]
    num_overpasses = np.load(f)
    num_groundsites = np.load(f)
    num_iterations = np.load(f)
    num_iterations = num_iterations[0]

    for k in range(num_iterations):
        for ng in range(len(num_groundsites)):
            for no in range(len(num_overpasses)):
                val = np.load(f)
                num_gs = val[0]
                num_op = val[1]
                k = val[2]
                k = int(k)
                fo = val[3]
                fp = val[4]
                nit = val[5]
                xt = np.load(f)
                xe = np.load(f)
                xo = np.load(f)
                fovals[k,ng,no] = fo
                fpvals[k,ng,no] = fp
                xerr[k,ng,no] = np.linalg.norm(xt - xo)        # compute norm
                xerr[k,ng,no] = xerr[k,ng,no] * xerr[k,ng,no]  # square square norm
                print([num_gs, num_op])
                    # print(xt)
                    # print(xo)
                    # print(' ')
