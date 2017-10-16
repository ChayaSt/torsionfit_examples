from torsionfit.database import qmdatabase as ScanSet
from torsionfit import parameters as par
from parmed.charmm import CharmmParameterSet
import numpy as np
import itertools
import tqdm

param_to_opt=[('CG331', 'CG321', 'CG321', 'CG331')]
param = CharmmParameterSet('../../data/charmm_ff/top_all36_cgenff.rtf',
                           '../../data/charmm_ff/par_all36_cgenff.prm')
structure = '../structure/butane.psf'
scan = '../torsion_scans/MP2_torsion_scan/'
# Print initial guess

# Create a butane scan with torsions on (to compare for difference potential)
butane_scan = ScanSet.parse_psi4_out(scan, structure, pattern='*.out2')
butane_scan.compute_energy(param)
optimized = butane_scan.remove_nonoptimized()
optimized.compute_energy(param)

# Turn off torsion
dih_list = [('CG331', 'CG321', 'CG321', 'HGA2'),
             ('CG331', 'CG321', 'CG321', 'CG331'),
             ('HGA2', 'CG321', 'CG321', 'HGA2')]

param_tor_off = par.turn_off_params(param, dihedral=dih_list)

# Create butane scan with torsions off
optimized_0 = butane_scan.remove_nonoptimized()
optimized_0.compute_energy(param_tor_off)

optimized.build_phis(dih_list)

models = []
for i in itertools.product((0, 1, -1), repeat=6):
    models.append(i)

n = np.array([1., 2., 3., 4., 5., 6.])
Fourier_sums = {}
Fourier_transform = {}
for t in optimized.phis:
    inner_sum = (1 + np.cos(optimized.phis[t][:, np.newaxis]*n[:, np.newaxis])).sum(-1)
    Fourier_sums[t] = []
    Fourier_transform[t] = []
    for i in models:
        Fourier_sum = (i*inner_sum).sum(1)
        rel = Fourier_sum - min(Fourier_sum)
        fft = np.fft.rfft(rel)
        Fourier_sums[t].append(rel)
        Fourier_transform[t].append(fft.real[1:7])

sum_comb = []
for i in itertools.product((range(len(models))), repeat=3):
    sum_comb.append(i)

sum_all = np.zeros((len(sum_comb), 36))
for j, s in tqdm.tqdm(enumerate(sum_comb)):
    for i, t in enumerate(dih_list):
        sum_all[j] += Fourier_sums[t][s[i]]

np.save('fsum_all', sum_all)

