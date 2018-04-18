import json
import os
import fileinput
from fragmenter import utils, torsions
from openeye import oechem
from openmoltools import openeye

output_path = os.path.abspath('.')
input_path = os.path.abspath('../clinical_kinase_inhibitors_tagged.smi')
# Load mols from .smi
mollist = utils.to_oemol(input_path, title='title', verbose=False)

json_data = {}
json_data["driver"] = "property"
json_data["kwargs"] = {"properties": ["WIBERG_LOWDIN_INDICES", "MAYER_INDICES"]}
json_data["method"] = "hf3c"
json_data["options"] = {"BASIS": "def2-svp"}
json_data["return_output"] = "True"

for mol in mollist:
    name = mol.GetTitle()
    print('\nGenerating input for {}'.format(name))
    try:
        os.mkdir(os.path.join(output_path, name))
    except FileExistsError:
        print("Overwriting existing directory")
    conformers = openeye.generate_conformers(mol)
    tagged_smiles = oechem.OEMolToSmiles(mol)
    json_data["tagged_smiles"] = tagged_smiles
    molecule, atom_map = torsions.get_atom_map(tagged_smiles, conformers, is_mapped=True)
    if not atom_map:
        print("Can't get atom map. Skipping {}".format(name))
        continue
    print("{} has {} conformers".format(name, conformers.GetMaxConfIdx()))
    # Generate mol2 file
    openeye.molecule_to_mol2(conformers, tripos_mol2_filename='{}.mol2'.format(name), conformer=None)
    # Generate xyz file
    #xyz = utils.to_mapped_xyz(conformers, atom_map=atom_map, xyz_format=True, filename=name)

    xyz = utils.to_mapped_xyz(conformers, atom_map=atom_map)
    for i, coords in enumerate(xyz.split('*')):
        json_data['molecule'] = coords
        json_filename = "{}/{}_{}.input.json".format(name, name, str(i))
        with open(json_filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4, sort_keys=True)
        input_filename = os.path.join(os.getcwd(), json_filename)
        # replace command on psub script
        with open('bond_order_bsub.lsf', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('REPLACE', ' {}'.format(input_filename))

        bsub_file = os.path.join(os.getcwd(), '{}/{}_{}_bond_order.lfs'.format(name, name, str(i)))
        with open(bsub_file, 'w') as file:
            file.write(filedata)
        #change directory and submit job

# import numpy as np
# times = np.asarray(atom_map_time)
# np.save('ss_time', times)
# import matplotlib.pyplot as plt
# plt.hist(atom_map_time)
# plt.xlabel('Time (seconds)')
# plt.title("distribution of substructure search time")
# plt.savefig('ss_time.png')





