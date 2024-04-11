import os
import glob
import csv
import subprocess

# Locate necesary files and folders
input_path=input("Type or paste your genome's folder (then hit enter): ")
output_path=input("Type or paste the path for your results folder: ")

# Identify all protein-fasta files (G_n.faa) within our input_path
finder = "find "+input_path+" -not -iname '*minimal*' -not -iname '*piPolBs*' -not -iname '*truncated*' -not -iname '*complete*' -iname '*.faa'"
command = "parallel -j 30 amrfinder --protein {} --output {}_amrf.csv"
subprocess.run(finder+" | "+command, shell=True)

# Merge CSV files
header = ["Protein identifier	Gene symbol	Sequence name	Scope	Element type	Element subtype	Class	Subclass	Method	Target length	Reference sequence length	% Coverage of reference sequence	% Identity to reference sequence	Alignment length	Accession of closest sequence	Name of closest sequence	HMM id	HMM description"]
with open("{}/".format(output_path)+"AMRfinder_output.csv", "w") as out_file_csv:
    writer = csv.writer(out_file_csv)
    writer.writerow(header)
    #This identifies all json files within our directory
    files = glob.glob(input_path+'/**/*_amrf.csv', recursive = True)
    for file in files:
        with open (file, "r") as in_file_csv:
            reader = csv.reader(in_file_csv)
            next(reader)
            for line in reader:
                if "G_" in line:
                    writer.writerow(line)
                else:
                    print("Abnormality detected in:\n"+os.getcwd(file))
                    writer.writerow("Abnormality detected in:\n"+os.getcwd(file))
                    writer.writerow(line)
                    



# EXAMPLES:

# Command line 1 should look like this:
# find genomas -not -iname '*minimal*' -not -iname '*piPolBs*' -iname '*.faa' | parallel -j 30 amrfinder --protein {} --output {}_amrf.csv

# Command line 2 should look like this:
# find genomas -iname '*amrf.csv' | parallel -j 30 mv {} amrf_reslutados
