"""
simulation_box_size.py
----------------------
Read the box size (x, y, z) of each plate simulation from its prmtop
(%FLAG BOX_DIMENSIONS, i.e. the starting box, not per frame) and write one
table (300 K, 5.4 - 15.0 A, 0.2 A steps). Missing topologies are skipped.

Runs on : PC
Inputs  : /gibbs/arghavan/plate_simulations/<T>K/<d_nm>/topol_edited.prmtop
Outputs : utils/results_pc/plate_box_dimensions.dat   (distance, x, y, z in A)
Usage   : python simulation_box_size.py
Change  : T, DISTANCES_NM
"""
from pathlib import Path
import platform

# ---- where results go (automatic: laptop -> results_laptop, PC -> results_pc)
HERE = Path(__file__).resolve().parent
OUT = HERE / ("results_laptop" if platform.system() == "Darwin" else "results_pc")
OUTPUT_FILE = OUT / "plate_box_dimensions.dat"

# ---- inputs (raw simulations, outside the repo)
T = 300
SIM_DIR = Path(f"/gibbs/arghavan/plate_simulations/{T}K")
DISTANCES_NM = [f"{i / 100:.2f}" for i in range(54, 151, 2)]   # "0.54" ... "1.50"


def read_box_dimensions(top_file):
    """Return (x, y, z) in A from a prmtop, or None if not found.

    In a prmtop the block looks like:
        %FLAG BOX_DIMENSIONS
        %FORMAT(5E16.8)
          beta   x   y   z
    """
    lines = Path(top_file).read_text().splitlines()
    for i, line in enumerate(lines):
        if line.startswith("%FLAG BOX_DIMENSIONS"):
            values = lines[i + 2].split()
            _beta, x, y, z = (float(v) for v in values[:4])
            return x, y, z
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w") as out:
        out.write("Box dimensions for each plate simulation\n")
        out.write(f"{'distance(Å)':<12}{'x(Å)':<12}{'y(Å)':<12}{'z(Å)':<12}\n")

        for d in DISTANCES_NM:
            top_file = SIM_DIR / d / "topol_edited.prmtop"
            if not top_file.exists():
                print(f"Missing: {top_file}")
                continue

            box = read_box_dimensions(top_file)
            if box is None:
                print(f"Could not find BOX_DIMENSIONS in {top_file}")
                continue

            x, y, z = box
            out.write(f"{float(d) * 10:<12.1f}{x:<12.3f}{y:<12.3f}{z:<12.3f}\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
