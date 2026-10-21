"""
gist-remove-edges.py
--------------------
Remove the GIST voxels within 2.5 A of each box boundary (whole-box grid,
5.4 - 15.0 A, 0.2 A steps) and save the remaining voxels with both header lines.

Runs on : PC
Inputs  : GIST_DIR/gist_results/<d_A>/d-<d_A>-output.dat
Outputs : GIST_DIR/gist_results/<d_A>/d-<d_A>-output-edge-eliminated.dat   (next step: gist-makedx.bash)
Usage   : python gist-remove-edges.py
Change  : DISTANCES_A, X_LIMITS, Y_LIMITS, Z_LIMITS, GIST_DIR
"""
from pathlib import Path

import pandas as pd

GIST_DIR = Path("/gibbs/arghavan/TODO_gist_dir")   # set later
RESULTS_DIR = GIST_DIR / "gist_results"

DISTANCES_A = [f"{i / 10:.1f}" for i in range(54, 151, 2)]   # "5.4" ... "15.0"
X_LIMITS = (2.5, 47.5)   # A, strict (> and <)
Y_LIMITS = (2.5, 47.5)
Z_LIMITS = (2.5, 77.5)


def main():
    for d in DISTANCES_A:
        input_file = RESULTS_DIR / d / f"d-{d}-output.dat"
        output_file = RESULTS_DIR / d / f"d-{d}-output-edge-eliminated.dat"

        with open(input_file) as f:
            first_header = f.readline().rstrip()
            second_header = f.readline().rstrip()
        cols = second_header.split()
        df = pd.read_csv(input_file, sep=r"\s+", names=cols, skiprows=2, comment="#")

        keep = (
            (df["xcoord"] > X_LIMITS[0]) & (df["xcoord"] < X_LIMITS[1])
            & (df["ycoord"] > Y_LIMITS[0]) & (df["ycoord"] < Y_LIMITS[1])
            & (df["zcoord"] > Z_LIMITS[0]) & (df["zcoord"] < Z_LIMITS[1])
        )
        subset = df[keep]

        with open(output_file, "w") as f:
            f.write(first_header + " | Edge voxels within 2.5Å of each box boundary were excluded.\n")
            f.write(second_header + "\n")
            subset.to_csv(f, sep="\t", index=False, header=False, float_format="%.8f")
        print(f"d = {d} A: kept {len(subset)} of {len(df)} voxels")


if __name__ == "__main__":
    main()
