import pandas as pd
from fragmenter import utils
# Import FDA approved kinase inhibitors (As of Jan 2018)
kinase_inhibitors = pd.read_csv('clinical-kinase-inhibitors.csv')

# Generate smi input file
smiles = []
for i, inhibitor in kinase_inhibitors.iterrows():
    smiles.append("{} {}".format(inhibitor['smiles'], inhibitor['inhibitor']))

# Write out file
out_dir = '/Users/chayastern/src/ChayaSt/torsionfit_examples/kinase_inhibitors'
base_fname = 'clinical_kinase_inhibitors'
input_smi = utils.to_smi(smiles, out_dir, base_fname, return_fname=True)

# Generate index-tagged explicit hydrogen smiles
utils.mol_to_tagged_smiles('clinical_kinase_inhibitors.smi', 'clinical_kinase_inhibitors_tagged.smi')