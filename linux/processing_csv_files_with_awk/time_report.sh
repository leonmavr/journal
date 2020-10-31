#!/bin/bash

for d in `find ./data -mindepth 1 -maxdepth 1 -type d`;do
	echo -e "===== folder $d ====="
	awk -F"," 'BEGIN {sum=0;} 1!=2 {sum+=$2;} END {printf "mean = %.2f\n", sum/NR;}' $d/*.csv 
	awk -F"," 'BEGIN {sum=0; min=99999999;} 1!=2 {if ($2 < min) min=$2;} END {printf "min = %.2f\n", min;}' $d/*.csv 
	awk -F"," 'BEGIN {sum=0; max=00000000;} 1!=2 {if ($2 > max) max=$2;} END {printf "max = %.2f\n", max;}' $d/*.csv 
done
