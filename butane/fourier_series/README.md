## Cancellation of terms in torsion functional

The functional for torsion energy is given as follows:

![](fourier_series.png?raw=true)

Where n is the frequency, m is the torsion type and i is the torsion. In this work, 
n is truncated at 6.

When only one torsion of a specific torsion type exists in molecule, the curve that
arises from adding the frequencies for that torsion is usually as expected. 
`CG331_CG321_CG321_CG331_sparse.pdf` shows the curves for each frequency with `K_n=1`
for the C3-C2-C2-C3 torsion type in butane with torsion angles from 0 - 2pi. 
`CG331_CG321_CG321_CG331.pdf` shows all different combinations possible with each K
being either 0, 1 or -1. While the sums are unique, some are pretty similar in energy as 
seen in `CG331_CG321_CG321_CG331_sim_e.pdf`

However, the H2-C3-C3-H2 torsion type occurs 4 times in butane. When the C3-C2-C2-C3
torsion type angle goes from 0-2pi, 2 of the H2-C3-C3-H2 torsion type angles go from 0-2pi 
one will go from 2 radians to 2 radians and the other will go from -2 to -2
radians. Therefore, when the torsions are added, different frequencies will amplify or
cancel each others in different ways. 
In the C3-C2-C2-H2 torsion type, 2 torsions will fo from 0 to 0 and 2 will go from pi to pi. 

`HGA2_CG321_CG321_HGA2_sparse.pdf` and `CG331_CG321_CG321_HGA2_sparse.pdf` show how 
frequency sums for the torsions. 

Given that not all torsions in a molecule go from 0-2pi as the central rotatable bond
is rotated from 0-2pi, and that the phase shift is restrained to be only 0 or pi to 
retain symmetry around 0 and pi so that the same torsion type can be used in enantiomer,
the terms in the Fourier series will combine in such a way that some terms will exactly 
cancel each others out in certain situations. This leads to several models that have the 
same energy profile as seen in `sparse_sim.pdf`. The legend is given as the integer
of the frequency that was on for the torsion type C3-C2-C2-C3, H2-C2-C2-H2 and C3-C2-C2-H2. 
For this analysis, only one frequency term was used per torsion type. The K was either 1 or -1.
The -1 was included to account for the 180 phase shift. On the first page in `sparse_sim.pdf`,
the sum of all torsions is less than 0.5 for the entire sum; all terms essentially cancel each 
others out. It's interesting to note the combination of frequencies for the specific torsion types
that lead to this result. If all torsion types have the same frequency, they will all cancel each 
other unless the frequency is 6. 

This is relevant here because it explains why the posteriors seem so inconsistent. That happens
because there are so many models that can give essentially the same energy profile.  
