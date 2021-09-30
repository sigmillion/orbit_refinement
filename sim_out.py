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

        fovals = np.ndarray((num_iterations,len(num_groundsites),len(num_overpasses)))
        fpvals = np.ndarray((num_iterations,len(num_groundsites),len(num_overpasses)))
        xerr = np.ndarray((num_iterations,len(num_groundsites),len(num_overpasses)))
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
                # print([num_gs, num_op, np.mean(fovals), np.std(fovals), np.mean(fpvals), np.std(fpvals), np.sqrt(np.mean(xerr))])
        print(fovals)
        print(" ")
        print(fpvals)
        print(" ")
        print(xerr)

        for ng in range(len(num_groundsites)):
            for no in range(len(num_overpasses)):
                print("[gs, op] = [",num_groundsites[ng],",",num_overpasses[no],"]");
                print([np.mean(np.squeeze(fovals[:,ng,no]))/(num_groundsites[ng]*num_overpasses[no]),
                       np.std(np.squeeze(fovals[:,ng,no]))/(num_groundsites[ng]*num_overpasses[no]),
                       np.mean(np.squeeze(fovals[:,ng,no]))/(num_groundsites[ng]*num_overpasses[no]),
                       np.std(np.squeeze(fovals[:,ng,no]))/(num_groundsites[ng]*num_overpasses[no]),
                       np.sqrt(np.mean(np.squeeze(xerr[:,ng,no]))/(num_groundsites[ng]*num_overpasses[no]))])
                
