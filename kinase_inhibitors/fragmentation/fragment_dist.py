import matplotlib.pyplot as plt
import numpy as np

from openeye import oechem
from openforcefield.utils import read_molecules

# Load fragments
frag_list_1 = read_molecules('nrotor_1.smi')
frag_list_2 = read_molecules('nrotor_2.smi')
frag_list_3 = read_molecules('nrotor_3.smi')
frag_list_4 = read_molecules('nrotor_4.smi')
frag_list_5 = read_molecules('nrotor_5.smi')

all_frags = [frag_list_1, frag_list_2, frag_list_3, frag_list_4, frag_list_5]

rotors = {}
for i, frag_set in enumerate(all_frags):
    rotors[i+1] = len(frag_set)

n_frags = sum(rotors.values())
print(n_frags)

# Plot n rotor counts
plt.bar(list(rotors.keys()), list(rotors.values()), label='N_tot: {}'.format(n_frags));
plt.xlabel('rotors')
plt.ylabel('Counts')
plt.title('Rotatable bonds in kinase fragment set')
plt.legend();
plt.savefig('rot_bonds.png')
plt.close()

frag_size = {}
h_atoms = []
for i, frag_set in enumerate(all_frags):
    frag_size[i+1] = np.zeros(len(frag_set))
    for j, frag in enumerate(frag_set):
        atoms = frag.NumAtoms()
        h_atoms.append(atoms)
        frag_size[i+1][j] = atoms

plt.hist(h_atoms, label='{} fragments'.format(n_frags));
plt.xlabel('Heavy atoms')
plt.ylabel('Count')
plt.title('Distribution of heavy atoms in fragments');
plt.legend()
plt.savefig('heavy_atoms.png')
plt.close()

for frag_set in frag_size:
    plt.hist(frag_size[frag_set], label='{} rotors'.format(frag_set), alpha=0.2)
plt.xlabel('heavy atoms')
plt.ylabel('Counts')
plt.title('Heavy atoms for n_rotors')
plt.legend()
plt.savefig('heavy_atoms_rotor.png')
plt.close()
