#!/bin/bash
# remove_unnecessary_files.bash
# -----------------------------
# EXAMPLE kept for reference: PERMANENTLY DELETES intermediate GIST files
#   *-edge-removed.dx  and  *-edge-eliminated.out
# from each distance folder (5.4 - 15.0 A, 0.2 A steps; top level only, not subfolders).
# Missing distance folders are skipped.
#
# Runs on : PC
# Acts on : /gibbs/arghavan/gist_hydrophobic_plates/gist_results/<d_A>/   (no output files)
# Usage   : bash remove_unnecessary_files.bash
# Change  : base_path, the seq range (54 2 150 = 5.4..15.0 A), the -name patterns
# Tip     : replace -delete with -print for a dry run first.

base_path='/gibbs/arghavan/gist_hydrophobic_plates/gist_results/'

# Distances: 5.4, 5.6, ..., 15.0 Å
for i in $(seq 54 2 150); do
    distance_angstrom=$(awk -v i="$i" 'BEGIN {printf "%.1f", i/10}')
    work_dir="${base_path}${distance_angstrom}"

    if [[ ! -d "$work_dir" ]]; then
        echo "Skipping missing directory: $work_dir"
        continue
    fi

    echo "=== Cleaning d=${distance_angstrom} Å ==="

    find "$work_dir" -maxdepth 1 -type f \( \
        -name '*-edge-removed.dx' -o \
        -name '*-edge-eliminated.out' \
    \) -delete
done
