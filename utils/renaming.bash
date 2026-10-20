#!/bin/bash
# renaming.bash
# -------------
# EXAMPLE kept for reference: renames GIST job folders
#   arghavan.omp_<d>_0.5.<jobid>  ->  <d>      (e.g. arghavan.omp_9.2_0.5.123 -> 9.2)
#
# Runs on : PC
# Acts on : /gibbs/arghavan/gist_hydrophobic_plates/gist_results/  (renames in place, no output files)
# Usage   : bash renaming.bash
# Change  : the cd path, the glob (arghavan.omp_*_0.5.*) and the sed pattern
# Tip     : uncomment the `echo mv` line and comment out `mv` for a dry run first.

cd /gibbs/arghavan/gist_hydrophobic_plates/gist_results/
for dir in arghavan.omp_*_0.5.*; do
    newname=$(echo "$dir" | sed -E 's/^arghavan\.omp_([0-9.]+)_0\.5\..*/\1/')
    # echo mv "$dir" "$newname"
    mv "$dir" "$newname"
done
