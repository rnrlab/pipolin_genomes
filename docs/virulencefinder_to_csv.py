import os
import glob
import json
import csv
import subprocess

#This imput tells the program where are the files we want to analyze
input_path=input("Type or paste your genome's folder (then hit enter): ")
output_path=input("Type or paste the path for your results folder: ")

#This values are important for the writing of the csv file, might indent them there in the future
header=["Genome","virulence_ent","listeria","s.aureus_hostimm","s.aureus_exoenzyme","s.aureus_toxin","virulence_ecoli","stx","virulence_entfm_entls"]
Cache=[]

#This identifies all fasta files (G_n.fa) within our directory
script_path = "/home/tfm/miniconda3/envs/virulencefinder/bin/new_virulencefinder.py"
db_path = "/mnt/disk2/databases/virulencefinder_db"
subprocess.run("find "+input_path+" -mindepth 2 -maxdepth 2 -iname '*.fa' | parallel -j 30 python3 "+script_path+" -i {} -o "+output_path+" -p "+db_path+" -l 0.4 -t 0.7", shell=True)

#This monstuosity prints each data.json as a row in a single csv file
with open(output_path+"/virulencefinder_output.csv", "w") as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(header)
    #This identifies all json files within our directory
    files = glob.glob(output_path+'/**/*.json', recursive = True)
    for file in files:
        with open (file, "r") as file_json:
            data = json.load(file_json)
            results = data["new_virulencefinder"]["results"]
            #This is a list of the scores given by VirulenceFinder
            Ent1 = results["Enterococcus"]
            Lister = results["Listeria"]
            Saur = results["S. aureus"]
            Ecoli = results["Escherichia coli"]
            Ent2 = results["Enterococcus faecium & Enterococcus lactis"]
            #We obtain the name of the Genome from the data.json
            genome_base = os.path.basename(file)
            genome_name = (os.path.splitext(genome_base)[0])
            Cache.append(genome_name)
            for k in Ent1.items():
                Cache.append(k[1])
            for k in Lister.items():
                Cache.append(k[1])
            for k in Saur.items():
                Cache.append(k[1])
            for k in Ecoli.items():
                Cache.append(k[1])
            for k in Ent2.items():
                Cache.append(k[1])
            writer.writerow(Cache)
            Cache=[]

# Remove each individual json file and tmp file
finder_1 = "find "+output_path+" -iname '*.json'"
command_1 = "parallel -j 30 rm {}"
finder_2 = "find "+output_path+" -iname '*_tmp'"
command_2 = "parallel -j 30 rm -r {}"
subprocess.run(finder_1+" | "+command_1, shell=True)
subprocess.run(finder_2+" | "+command_2, shell=True)
