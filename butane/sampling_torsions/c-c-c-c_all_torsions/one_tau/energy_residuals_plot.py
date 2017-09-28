
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from torsionfit.database import qmdatabase as ScanSet
from parmed.charmm import CharmmParameterSet, CharmmPsfFile
import torsionfit.parameters as par
import torsionfit.backends.sqlite_plus as db
from collections import OrderedDict
from torsionfit.backends import sqlite_plus
from matplotlib.backends.backend_pdf import PdfPages


# Turn off dihedral energy for to get residuals 
param = CharmmParameterSet('../../../../data/charmm_ff/par_all36_cgenff.prm', 
                           '../../../../data/charmm_ff/top_all36_cgenff.rtf')
structure = '../../../structure/butane.psf'
struct_parmed = CharmmPsfFile(structure)
scan = '../../../torsion_scans/MP2_torsion_scan/'

#dih_list = [('HGA2', 'CG321', 'CG331', 'HGA3'),
#             ('CG331', 'CG321', 'CG321', 'HGA2'),
#             ('CG331', 'CG321', 'CG321', 'CG331'),
#             ('CG321', 'CG321', 'CG331', 'HGA3'),
#             ('HGA2', 'CG321', 'CG321', 'HGA2')]
dih_list = [ ('CG331', 'CG321', 'CG321', 'HGA2'),
             ('CG331', 'CG321', 'CG321', 'CG331'),
             ('HGA2', 'CG321', 'CG321', 'HGA2')]

# Save another parameter set
param_tor_off = par.turn_off_params(param=param, structure=struct_parmed, dihedral=dih_list, copy=True)


# Load samplers
# dbs = OrderedDict()
# for i in range(25):
#     dbs['db_{}'.format(i)] = sqlite_plus.load('c-c-c-c_all_10000000_{}/c-c-c-c_all_10000000_{}.sqlite'.format(i, i))

butane = ScanSet.parse_psi4_out(scan, structure, pattern='*.out2')
optimized = butane.remove_nonoptimized()

optimized.compute_energy(param)
optimized.build_phis(dih_list)

without_tor = butane.remove_nonoptimized()
without_tor.compute_energy(param_tor_off)



# look at difference potential
new_param = CharmmParameterSet('../../../../data/charmm_ff/top_all36_prot.rtf',
                              '../../../../data/charmm_ff/par_all36_cgenff.prm')
new_struct = butane.remove_nonoptimized()
# parameterize with db_0
par.add_missing(param_list=dih_list, param=new_param, sample_n5=True)
par.set_phase_0(dih_list, new_param)
with PdfPages('Energy_residuals_rj_single.pdf') as pdf:
    # Update parameters
    for i in range(25):
        db = sqlite_plus.load('c-c-c-c_all_10000000_{}/c-c-c-c_all_10000000_{}.sqlite'.format(i, i))

        plt.figure()
        plt.subplot(1, 2, 1)
        par.update_param_from_sample(param_list=dih_list, param=new_param, db=db, n_5=True, rj=True, model_type='numpy')
        new_struct.compute_energy(new_param)

        plt.plot(optimized.angles, optimized.qm_energy, 'o', color='red', label='QM')
        plt.plot(optimized.angles, without_tor.mm_energy, color='blue', label='Before fit')
        plt.plot(optimized.angles, new_struct.mm_energy, '*', color='green', label='Fit')
        plt.plot(optimized.angles, optimized.mm_energy, '.', color='orange', label='Charmm')
        plt.ylabel('Relative Energy (KJ/mol)')
        plt.xlabel('Dihedral Angle (Degrees)')
        plt.title('Energy {}'.format(db))

        plt.legend()
        
        # Check
        plt.subplot(1, 2, 2)
        plt.plot(optimized.angles, without_tor.delta_energy, color='blue', label='Before fit')
        plt.plot(optimized.angles, optimized.delta_energy, color='orange', label='Charmm')
        plt.plot(optimized.angles, new_struct.delta_energy, color='green', label='Fit')
        plt.legend()
        plt.title('Residual Energy {}'.format(db))
        pdf.savefig()
        plt.close()
        del db





