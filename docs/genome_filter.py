import os

Filter_List = open("integron_filtering.txt", "w")

# The filter_results dir is where the results of integron_filtering.sh will be stored
os.chdir("filter_results")

Filtered_Genomes = os.listdir()
for item in Filtered_Genomes:
    base = os.path.basename(item)
    name = (os.path.splitext(base)[0])
    name = (os.path.splitext(name)[0])
    Filter_List.write(name+"\n")

Filter_List.close()
