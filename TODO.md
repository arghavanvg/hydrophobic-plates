# TODO: hydrophobic-plates repo migration

Old code: `~/lab/hydrophobic-plates-analysis` · Old results: `~/lab/hp-results` (laptop), `/gibbs/arghavan/hp-results-pc` (PC)

## To adjust later
- [ ] **gist-preprocessing**: set `GIST_DIR` (folder with `gist_results/<d_A>/`) in `gist-remove-edges.py` and `gist-makedx.bash`.
- [ ] **gist-preprocessing**: set `GZ_GIST_DIR` (folder with `300K_<d_nm>/gZ-output.dat`) in `gist-crop-between-plates.py`.
- [ ] **gZ**: set `GZ_DATA_DIR` (PC path of the `<d>.out` files) in all 4 notebooks.
- [ ] **gZ**: write code that creates the `<d>.out` files (currently made manually; 2 columns: x, summed O count per 170×170 y-z slab).
- [ ] **gZ / one-plate-interference**: add the second "6–15 Å" cell (zero-density fix with `tol`; old `gZ_plot.ipynb` cell 11).
- [ ] **one-plate**: put the original `gZ-one-plate-300K-leftSide.dat` / `-rightSide.dat` in `one-plate/results_pc/`, then run `one-plate-average-gZ.py` (makes `one-plate-gZ-averaged-left/right.dat`, needed by the 3 gZ interference notebooks).
- [ ] **utils/add-pptx.ipynb**: image folders still point to Dropbox; switch to the new `gZ/results_pc/...` folders, and decide laptop vs PC.
- [ ] **utils/no_wat.py**: may be repetitive; drop later?
- [ ] **water-count**: add the number-of-waters plot (old `add-pptx.ipynb` cells 2–3).
- [ ] **Shared code**: duplicated functions (`load_trajectory`, `get_plate_boundaries`, `count_waters_per_frame` in both water counters; `emit` in 4 files).
- [ ] **.gitignore**: add rules for large outputs (`.dx`, trajectories, `gist-preprocessing/results_pc/gist-plates-*/`) before committing results.

## Folders
- [x] `utils/`: done (committed by you)
- [x] `gist-preprocessing/plates_gist_input_notes.md`
- [x] `gZ/`: 4 notebooks added (`GZ_DATA_DIR` still a placeholder, see above)
- [x] `one-plate/`: one-plate-average-gZ.py, one-plate-peaks.ipynb, bulk-water-rdf.ipynb
- [x] `gist-preprocessing/`: make-gist-jobs.py, gist-crop-between-plates.py, gist-remove-edges.py, gist-makedx.bash, plates_gist_input_notes.md
- [ ] `Eww-sw-interaction/`: gistpp_Eww_calculation_09-04, gist-interactionEnergy-Eww-Esw-calculation
- [ ] `neighbors/`: gist_nbrs.bash
- [ ] `hbonds/`: no code in old repo (results in `hp-results/hbond_data`)
- [ ] `entropy/`: entropy_calculation, entropy_correction_test
- [ ] `pairwise-energies/`: pairwise_energies, pair_energy_for_bulk, plot_pairwise_energies, split-space-in-two.py, plot_split_energies.py
- [ ] `wall-LJ-energy/`: wall-LJ-energies
- [ ] `water-count/`: water_counter.py, confined-water-counter.py, volume
- [ ] `meniscus/`: meniscus-finder.py, meniscus-y-axis.py, meniscus-plot
- [ ] `energy-analysis/`: df-energy-plotting, read_results_DataFrame

## Housekeeping
- [ ] **Make the GitHub repo private** before generating/committing data (Settings → General → Danger Zone → Change visibility)
- [ ] PC: `git clone git@github.com:arghavanvg/hydrophobic-plates.git` in `/gibbs/arghavan`
- [ ] Send the PC file listing (`pc_dirs.txt`, `pc_files.txt`) to `~/lab/claude-temp/`
- [ ] Sort loose old results: `hp-results/` (pmf.png, contribution.png, hp-data.csv, .dx files), `hp-results-pc/plots/`
- [ ] Delete `~/lab/claude-temp/` when migration is done
