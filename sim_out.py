import numpy as np


if __name__ == "__main__":
    # Load data
    with open('data.npy', 'rb') as f:
        seed_val = np.load(f)
        seedd_val = seed_val[0]
        num_overpasses = np.load(f)
        num_groundsites = np.load(f)
        num_iterations = np.load(f)
        num_iterations = num_iterations[0]

        for no in range(len(num_overpasses)):
            for ng in range(len(num_groundsites)):
                fovals = np.ndarray((num_iterations,))
                fpvals = np.ndarray((num_iterations,))
                xerr = np.ndarray((num_iterations,))
                for k in range(num_iterations):
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
                    fovals[k] = fo
                    fpvals[k] = fp
                    xerr[k] = np.linalg.norm(xt - xo)
                    xerr[k] = xerr[k] * xerr[k]
                    # print(xt)
                    # print(xo)
                    # print(' ')
                print([num_gs, num_op, np.mean(fovals), np.std(fovals), np.mean(fpvals), np.std(fpvals), np.sqrt(np.mean(xerr))])
