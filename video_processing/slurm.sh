#!/usr/bin/env bash
#SBATCH --job-name=odm # Job name
#SBATCH --output=logs/odm_log_%j.out
#SBATCH --ntasks=1                    # Run on a single Node
#SBATCH --cpus-per-task=10
#SBATCH --mem=160gb                     # Job memory request
#SBATCH --partition=compsci-gpu
#SBATCH --gres=gpu:2
#SBATCH --mail-type=END                 
#SBATCH --mail-user=netid@duke.edu             # It will send you an email when the job is finished.

module load cuda

sh singularity.sh

