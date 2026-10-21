"""
make-gist-jobs.py
-----------------
Write a cpptraj GIST input (pme.in) and a Slurm submit script for every plate
distance (300 K, 5.4 - 15.0 A, 0.2 A steps), one folder per distance.

Runs on : PC
Inputs  : /gibbs/arghavan/plate_simulations/<T>K/<d_nm>/topol_edited.prmtop, <T>K_<d_nm>.nc
Outputs : /gibbs/arghavan/gist_hydrophobic_plates/<SPACING>-spacing/<d_nm>/pme.in   (e.g. 0.1-spacing)
          .../<SPACING>-spacing/<d_nm>/submit_gist.sbatch (mpi) or submit_OMP.sbatch (omp)
Usage   : python make-gist-jobs.py   (then sbatch the submit script in each folder)
Change  : SPACING (0.5 or 0.1), ENGINE ("mpi" or "omp"), N_CPUS
"""
from pathlib import Path

# ---- settings
SPACING = 0.1          # grid spacing (A): 0.5 or 0.1
ENGINE = "mpi"         # "mpi" (cpptraj.MPI) or "omp" (cpptraj.OMP)
N_CPUS = 8             # MPI tasks or OMP threads (old runs: 0.5 mpi = 4, 0.1 mpi = 8, 0.5 omp = 8)
T = 300
DISTANCES_NM = [f"{i / 100:.2f}" for i in range(54, 151, 2)]   # "0.54" ... "1.50"

JOBS_DIR = Path("/gibbs/arghavan/gist_hydrophobic_plates")      # jobs go in JOBS_DIR/<SPACING>-spacing/
SIM_DIR = Path(f"/gibbs/arghavan/plate_simulations/{T}K")
GRIDDIM = {0.5: "102 100 160", 0.1: "504 500 796"}[SPACING]     # covers the whole box


def pme_input(d, d_angstrom):
    return f"""parm {SIM_DIR}/{d}/topol_edited.prmtop
trajin {SIM_DIR}/{d}/{T}K_{d}.nc
gist pme refdens 0.03331284139 temp 300 gridspacn {SPACING}0 gridcntr 25 25.38 40 griddim {GRIDDIM} floatfmt double floatprec 8 prefix d-{d_angstrom} info Info.dat
go
"""


def sbatch_header(d_angstrom):
    if ENGINE == "mpi":
        return f"""#!/bin/bash
#SBATCH --job-name=gist_{d_angstrom}_{SPACING}
#SBATCH --out=job.slurm.out
#SBATCH --nodes=1
#SBATCH --ntasks={N_CPUS}
#SBATCH --nodelist=node010
#SBATCH --tasks-per-node={N_CPUS}
#SBATCH --time=3-00:00

module load cpptraj-mpi/gist-mpi
hostname
"""
    return f"""#!/bin/bash
#SBATCH --job-name=omp_{d_angstrom}_{SPACING}
#SBATCH --out=job.slurm.out
#SBATCH --nodes=1
#SBATCH --nodelist=node010
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task={N_CPUS}
#SBATCH --time=3-00:00
#SBATCH --mem=4gb

module load amber/24_OMP
hostname
"""


def run_command(d_angstrom):
    if ENGINE == "mpi":
        return f"mpirun -n {N_CPUS} /cm/shared/apps/cpptraj-mpi/bin/cpptraj.MPI -i pme.in > {d_angstrom}_cpptraj.log"
    return f"\nOMP_NUM_THREADS=$SLURM_CPUS_PER_TASK /cm/shared/apps/amber/24_openmp/bin/cpptraj.OMP -i pme.in > {d_angstrom}_cpptraj.log"


def sbatch_script(d_angstrom):
    return sbatch_header(d_angstrom) + f"""

# =========================================
# 1. Define directory names [DO NOT CHANGE]
# =========================================
# Get name of the user submitting the job
export PREFIX=`whoami`

# Get name of the temporary directory working directory, physically on the compute-node. If it doesnt exist yet, the script will make it
workdir="/local/$PREFIX.${{SLURM_JOB_NAME}}.${{SLURM_JOB_ID}}"

# Get submit directory (every file/folder below this directory is copied to the compute node)
submitdir="${{SLURM_SUBMIT_DIR}}"

# Get storage directory (where results will be saved at the end)
storingdir="/gibbs/$PREFIX"

echo "worker path is:"
echo $workdir
echo "submitdir path is:"
echo $submitdir
echo "storingdir path is:"
echo $storingdir

# ===================================
# 2. Transfer to node [DO NOT CHANGE]
# ===================================

# create/empty the temporary directory on the compute node
if [ ! -d "${{workdir}}" ]; then
  mkdir -p "${{workdir}}"
else
  rm -rf "${{workdir}}"/*
fi

# change current directory to the location of the sbatch command. "submitdir" is somewhere in the home directory on the head node
cd "${{submitdir}}"

# copy all files/folders in "submitdir" to "workdir"
cp -prf * ${{workdir}}

# change directory to the temporary directory on the compute-node
cd ${{workdir}}

# ====================================================
# 3. Computing commands [CHANGE ACCORDING TO YOUR JOB]
# ====================================================
{run_command(d_angstrom)}

# ==================================================================================================
# 4. Function to transfer back to the /gibbs/user (where log-term storage should be) [DO NOT CHANGE]
# ==================================================================================================

# Define clean-up function
function clean_up {{
  # - remove log-file on the compute-node, to avoid the one created by SLURM being overwritten
  rm job.slurm.out
  # - delete temporary files from the compute-node, before copying
  # rm -r ...
  # - change directory to where long-term storage is
  cd "${{storingdir}}"
  # - copy the temporary directory on the compute-node over
  cp -prf "${{workdir}}"/ .
  # - erase the temporary directory from the compute-node
  rm -rf "${{workdir}}"/*
  rm -rf "${{workdir}}"
  # - exit the script
  exit
}}

trap 'clean_up' EXIT

"""


def main():
    submit_name = "submit_gist.sbatch" if ENGINE == "mpi" else "submit_OMP.sbatch"
    for d in DISTANCES_NM:
        d_angstrom = round(float(d) * 10, 1)
        job_dir = JOBS_DIR / f"{SPACING}-spacing" / d
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "pme.in").write_text(pme_input(d, d_angstrom))
        (job_dir / submit_name).write_text(sbatch_script(d_angstrom))
    print(f"pme.in + {submit_name} written for {len(DISTANCES_NM)} distances in {JOBS_DIR / f'{SPACING}-spacing'}")


if __name__ == "__main__":
    main()
