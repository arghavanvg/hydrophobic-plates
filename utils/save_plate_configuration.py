"""
save_plate_configuration.py
---------------------------
Save the plate atoms (resname WALL) from frame 0 only of each plate
simulation as a PDB, one file per plate distance (300 K, 6.0 - 15.0 A, 0.2 A steps).

Runs on : PC
Inputs  : /gibbs/arghavan/plate_simulations/<T>K/<d_nm>/<T>K_<d_nm>.nc
          /gibbs/arghavan/plate_simulations/<T>K/<d_nm>/topol_edited.prmtop
Outputs : utils/results_pc/plate_configurations/<d_A>_plate_configuration.pdb
Usage   : python save_plate_configuration.py
Change  : T, DISTANCES_NM, FRAME (which frame to save)
"""
from pathlib import Path
import platform

import mdtraj as md

# ---- where results go (automatic: laptop -> results_laptop, PC -> results_pc)
HERE = Path(__file__).resolve().parent
OUT = HERE / ("results_laptop" if platform.system() == "Darwin" else "results_pc")
OUTPUT_DIR = OUT / "plate_configurations"

# ---- inputs (raw simulations, outside the repo)
T = 300
SIM_DIR = Path(f"/gibbs/arghavan/plate_simulations/{T}K")
DISTANCES_NM = [f"{i / 100:.2f}" for i in range(60, 151, 2)]   # "0.60" ... "1.50"
FRAME = 0                                                         # frame to save


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for d in DISTANCES_NM:
        d_angstrom = round(float(d) * 10, 1)
        traj_file = SIM_DIR / d / f"{T}K_{d}.nc"
        top_file = SIM_DIR / d / "topol_edited.prmtop"

        frame = md.load_frame(str(traj_file), top=str(top_file), index=FRAME)
        walls = frame.topology.select("resname WALL")

        out_file = OUTPUT_DIR / f"{d_angstrom}_plate_configuration.pdb"
        frame.atom_slice(walls).save_pdb(str(out_file))
        print(f"saved {out_file}")


if __name__ == "__main__":
    main()
