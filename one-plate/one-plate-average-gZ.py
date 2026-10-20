"""
one-plate-average-gZ.py
-----------------------
Average the one-plate water-oxygen density g_z(O) of the left side and the
mirrored right side, then save that average for the left side and its mirror
image for the right side.

Runs on : PC
Inputs  : one-plate/results_pc/gZ-one-plate-300K-leftSide.dat    (x = 0.05 ... 13.55 A)
          one-plate/results_pc/gZ-one-plate-300K-rightSide.dat   (x = -13.55 ... -0.05 A)
          header "x(Angstrom)  g_z(O)"; you add these files yourself
Outputs : one-plate/results_pc/one-plate-gZ-averaged-left.dat    (x = 0.05 ... 13.55 A)
          one-plate/results_pc/one-plate-gZ-averaged-right.dat   (x = -13.55 ... -0.05 A)
          columns: x(Angstrom)  gO(z)_total
Usage   : python one-plate-average-gZ.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "results_pc"


def main():
    left = pd.read_csv(OUT / "gZ-one-plate-300K-leftSide.dat", sep=r"\s+", header=0)
    right = pd.read_csv(OUT / "gZ-one-plate-300K-rightSide.dat", sep=r"\s+", header=0)

    x_left = left.iloc[:, 0].astype(float).round(2).values
    x_right = right.iloc[:, 0].astype(float).round(2).values

    # mirror the right side so both run from the plate outward, then average
    g_avg = (left.iloc[:, 1].values + right.iloc[:, 1].values[::-1]) / 2

    header = "x(Angstrom)\tgO(z)_total"
    np.savetxt(OUT / "one-plate-gZ-averaged-left.dat",
               np.column_stack((x_left, g_avg)), fmt=["%.2f", "%.16g"], delimiter="\t", header=header, comments="")
    np.savetxt(OUT / "one-plate-gZ-averaged-right.dat",
               np.column_stack((x_right, g_avg[::-1])), fmt=["%.2f", "%.16g"], delimiter="\t", header=header, comments="")
    print(f"saved averaged-left and averaged-right in {OUT}")


if __name__ == "__main__":
    main()
