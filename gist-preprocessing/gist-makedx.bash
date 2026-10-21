#!/bin/bash
# gist-makedx.bash
# ----------------
# Turn each edge-eliminated GIST table into .dx maps with gistpp makedx
# (whole-box grid, 5.4 - 15.0 A, 0.2 A steps). Missing distance folders are skipped.
# The .dat table is first renamed to .out (gistpp input).
#
# Runs on : PC (needs module gistpp)
# Inputs  : GIST_DIR/gist_results/<d_A>/d-<d_A>-output-edge-eliminated.dat   (from gist-remove-edges.py)
#           d-<d_A>-<quantity>.dx (grid template for each map)
# Outputs : GIST_DIR/gist_results/<d_A>/d-<d_A>-<quantity>-edge-removed.dx for
#           gO (col 05), dTStrans-dens (08), dTSorient-dens (10), dTSsix-dens (12),
#           neighbor-dens (24), neighbor-norm (25)
# Usage   : bash gist-makedx.bash
# Change  : GIST_DIR, the seq range (54 2 150 = 5.4..15.0 A), the quantities/columns

module load gistpp

GIST_DIR='/gibbs/arghavan/TODO_gist_dir'   # set later
base_path="${GIST_DIR}/gist_results/"

# ints = range(54, 151, 2) -> distances 5.4, 5.6, ..., 15.0 Å
for i in $(seq 54 2 150); do
    distance_angstrom=$(awk -v i="$i" 'BEGIN {printf "%.1f", i/10}')
    work_dir="${base_path}${distance_angstrom}"

    if [[ ! -d "$work_dir" ]]; then
        echo "Skipping missing directory: $work_dir"
        continue
    fi

    echo "=== Processing d=${distance_angstrom} Å ==="
    cd "$work_dir" || continue

    mv "d-${distance_angstrom}-output-edge-eliminated.dat" "d-${distance_angstrom}-output-edge-eliminated.out"

    gistpp -i "d-${distance_angstrom}-output-edge-eliminated.out" \
           -i2 "d-${distance_angstrom}-gO.dx" \
           -op makedx -opt const 05 \
           -o "d-${distance_angstrom}-gO-edge-removed.dx"

    gistpp -i "d-${distance_angstrom}-output-edge-eliminated.out" \
           -i2 "d-${distance_angstrom}-dTStrans-dens.dx" \
           -op makedx -opt const 08 \
           -o "d-${distance_angstrom}-dTStrans-dens-edge-removed.dx"

    gistpp -i "d-${distance_angstrom}-output-edge-eliminated.out" \
           -i2 "d-${distance_angstrom}-dTSorient-dens.dx" \
           -op makedx -opt const 10 \
           -o "d-${distance_angstrom}-dTSorient-dens-edge-removed.dx"

    gistpp -i "d-${distance_angstrom}-output-edge-eliminated.out" \
           -i2 "d-${distance_angstrom}-dTSsix-dens.dx" \
           -op makedx -opt const 12 \
           -o "d-${distance_angstrom}-dTSsix-dens-edge-removed.dx"

    gistpp -i "d-${distance_angstrom}-output-edge-eliminated.out" \
           -i2 "d-${distance_angstrom}-neighbor-norm.dx" \
           -op makedx -opt const 24 \
           -o "d-${distance_angstrom}-neighbor-dens-edge-removed.dx"

    gistpp -i "d-${distance_angstrom}-output-edge-eliminated.out" \
           -i2 "d-${distance_angstrom}-neighbor-norm.dx" \
           -op makedx -opt const 25 \
           -o "d-${distance_angstrom}-neighbor-norm-edge-removed.dx"
done
