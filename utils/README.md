# utils

Small helper scripts. Outputs go to `results_laptop/` on the Mac and `results_pc/` on the PC (chosen automatically).

| File | Runs on | Inputs | Outputs |
|---|---|---|---|
| `save_plate_configuration.py` | PC | `/gibbs/arghavan/plate_simulations/300K/<d_nm>/` (.nc, prmtop; frame 0) | `results_pc/plate_configurations/<d_A>_plate_configuration.pdb` |
| `simulation_box_size.py` | PC | `/gibbs/arghavan/plate_simulations/300K/<d_nm>/topol_edited.prmtop` | `results_pc/plate_box_dimensions.dat` |
| `add-pptx.ipynb` | laptop | image folders | `results_laptop/all_plots.pptx` |
| `no_wat.py` | PC | Joe's pure-water GIST output and trajectory on `/avogadro` | none (may be dropped) |
| `renaming.bash` | PC | example: renames folders in `gist_results/` | none |
| `remove_unnecessary_files.bash` | PC | example: **deletes** edge-removed GIST files | none |

`d_nm` = distance in nm (e.g. `0.92`), `d_A` = distance in Å (e.g. `9.2`).
