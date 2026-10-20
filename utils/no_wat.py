"""
no_wat.py
Note: exploratory and possibly repetitive; may be dropped later.

Loads the GIST output of Joe's pure TIP4P/2005 water box at 300 K and prints
the number of waters. Saves nothing.

Runs on : PC
Inputs  : /avogadro/joe/pure_tip4p_sim/gist_300K_pure/pure_300K-output.dat
          /avogadro/joe/pure_tip4p_sim/300K/md.nc, topol.prmtop
Outputs : none (printed only)
Change  : file, base_path
"""
import mdtraj as md
import pandas as pd

file = '/avogadro/joe/pure_tip4p_sim/gist_300K_pure/pure_300K-output.dat'
base_path = '/avogadro/joe/pure_tip4p_sim/300K/'

with open(file) as f:
    lines = f.readlines()
cols = lines[1].strip().split()

df = pd.read_csv(file, sep=r'\s+', names=cols, skiprows=2, comment='#')
print(df)
print("mean population:", df['population'].mean())

traj = md.load(f'{base_path}md.nc', top=f'{base_path}topol.prmtop')
print(traj)
