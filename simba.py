import numpy as np
import sys

# as sysarg pass first the independednt variable and then all the dependent variables
# for example if you want to find relationship between ms and sfr and met
# you will call python main.py ms sf met

#             ms      (stellar mass)
#             sfr     (star formation rate)
#             met     (metallicity)
#             mHI     (H1 mass)
#             mH2     (H2 mass)
#             mbh     (black hole mass)
#             mdust   (dust mass)
#             mh      (dark matter halo mass)
#             rh      (dark matter half-mass radius)
#             sigh    (dark matter halo velocity dispersion)

map_sysargs_column = {'ms': 0, 'sfr': 1, 'met': 2, 'mHI': 3, 'mH2': 4, 'mbh': 5, 'mdust': 6, 'mh': 7, 'rh': 8, 'sigh': 9}

independent = 'ms'
dependents = ['sfr', 'met']

simba_100 = np.load('simba_list_100' + '.npy')

independent_col = simba_100[map_sysargs_column[independent]]
dependent_cols = simba_100[[map_sysargs_column[x] for x in dependents]]