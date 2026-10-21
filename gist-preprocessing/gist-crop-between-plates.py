"""
gist-crop-between-plates.py
---------------------------
Keep only the gZ-grid GIST voxels between the two plates, away from the plate
surfaces (X_CORRECTION) and the plate edges / meniscus (MENISCUS_CORRECTION).
Voxels must lie fully inside the region (half a voxel from each limit).

Runs on : PC
Inputs  : GZ_GIST_DIR/<T>K_<d_nm>/gZ-output.dat
Outputs : gist-preprocessing/results_pc/gist-plates-<T>K/<d_nm>/<d_A>-gist-output_parsed.dat
Usage   : python gist-crop-between-plates.py
Change  : DISTANCES_NM, X_CORRECTION, MENISCUS_CORRECTION, GZ_GIST_DIR
Note    : the y/z limits are the plate edges (fixed numbers, from the 9.4 A frame 0).
"""
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent / "results_pc"
GZ_GIST_DIR = Path("/gibbs/arghavan/TODO_gZ_gist_dir")   # set later

T = 300
DISTANCES_NM = ["0.82", "0.92"]
X_CORRECTION = 2.78          # A, from each plate surface
MENISCUS_CORRECTION = 4.00   # A, from each plate edge (y and z)
VOXEL_SIZE = 0.1             # A
X_CENTER = 25.00             # A
Y_EDGES = (16.83, 33.93)     # A, plate edges in y
Z_EDGES = (31.19, 48.81)     # A, plate edges in z


def main():
    half = VOXEL_SIZE / 2
    for distance in DISTANCES_NM:
        d = round(float(distance) * 10, 2)
        input_file = GZ_GIST_DIR / f"{T}K_{distance}" / "gZ-output.dat"
        output_file = OUT / f"gist-plates-{T}K" / distance / f"{d}-gist-output_parsed.dat"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        x_min, x_max = X_CENTER - d / 2 + X_CORRECTION, X_CENTER + d / 2 - X_CORRECTION
        y_min, y_max = Y_EDGES[0] + MENISCUS_CORRECTION, Y_EDGES[1] - MENISCUS_CORRECTION
        z_min, z_max = Z_EDGES[0] + MENISCUS_CORRECTION, Z_EDGES[1] - MENISCUS_CORRECTION

        with open(input_file) as f:
            f.readline()
            cols = f.readline().split()
        df = pd.read_csv(input_file, sep=r"\s+", names=cols, skiprows=2, comment="#")

        keep = (
            (df["xcoord"] >= x_min + half) & (df["xcoord"] <= x_max - half)
            & (df["ycoord"] >= y_min + half) & (df["ycoord"] <= y_max - half)
            & (df["zcoord"] >= z_min + half) & (df["zcoord"] <= z_max - half)
        )
        subset = df[keep]
        subset.to_csv(output_file, sep="\t", index=False, float_format="%.8f")
        print(f"Saved {len(subset)} voxels to '{output_file}'.")


if __name__ == "__main__":
    main()
