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
                vals = np.ndarray((num_iterations,))
                for k in range(num_iterations):
                    val = np.load(f)
                    num_gs = val[0]
                    num_op = val[1]
                    k = val[2]
                    k = int(k)
                    fo = val[3]
                    nit = val[4]
                    xt = np.load(f)
                    xe = np.load(f)
                    xo = np.load(f)
                    vals[k] = fo
                    # print(xt)
                    # print(xo)
                    # print(' ')
                print([num_gs, num_op, np.mean(vals), np.std(vals)])
