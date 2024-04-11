#!/usr/bin/env

# Directories index:
# all dirs used here are within one named integron, as well as the sh and py scripts.
# /Volumes/Trastero4/Results_EP/ is the dir with ALL your genomes.
# filter_results is the dir where we screen for positive results (py reads from here which G_n.fa to copy to the txt file).


source /Users/modesto/anaconda3/etc/profile.d/conda.sh
conda activate /Users/modesto/conda/envs/integron_filtering
cwd=$(pwd)
mkdir filter_results
cd /Users/modesto/Applications/integron-filtering
find /Volumes/Trastero4/Results_EP/ -mindepth 2 -maxdepth 2 -iname '*.fa' | parallel -j 30 ./IntI-screening.sh -i {} -m IntI-Cterm.hmm -t 8 -o $cwd/filter_results

cd $cwd
find filter_results -empty -or -iname '*.tab' | parallel -j 30 rm {}
python3 genome_filter.py
