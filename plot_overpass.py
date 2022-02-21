import numpy as np
import matplotlib.pyplot as plt

with open('range_true.npy', 'rb') as f:
    range_true = np.load(f)
with open('range_rate_true.npy', 'rb') as f:
    range_rate_true = np.load(f)
    
with open('range_est.npy', 'rb') as f:
    range_est = np.load(f)
with open('range_rate_est.npy', 'rb') as f:
    range_rate_est = np.load(f)

for i in range(2):
    print(range_rate_true[i,:])
    print(range_rate_est[i,:])

    ax1 = plt.subplot(121)
    ax1.plot(range_rate_true[i,:]/3,np.arange(0.0, 4.7, 4.7/(len(range_rate_true[i,:]))))
    ax1.plot(range_rate_est[i,:]/3,np.arange(0.0, 4.7, 4.7/(len(range_rate_est[i,:]))))
    ax1.set_ylabel('Time [minutes]')
    ax1.set_xlabel('Doppler Frequency [kHz/100MHz]')
    ax1.grid()
    ax2 = plt.subplot(122)
    ax2.plot(range_rate_true[i,:]/3-range_rate_est[i,:]/3,np.arange(0.0, 4.7, 4.7/(len(range_rate_true[i,:]))))
    ax2.set_ylabel('Time [minutes]')
    ax2.set_xlabel('Doppler Frequency [kHz/100MHz]')
    ax2.grid()
    
    #plt.show()

    plt.savefig("RangeRateOverpass.svg", dpi=300)
    break
