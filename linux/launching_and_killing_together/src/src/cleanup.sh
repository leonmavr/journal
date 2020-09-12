#!/bin/bash

output_file=/tmp/output.txt
> $output_file 

# --- trap handler
cleanup() {
	echo "Exit received. Cleaning up..."
	rm $output_file 
}
# ---

trap "cleanup" SIGINT SIGTERM EXIT


#--- main work 
for i in `seq 1 10`; do
	echo $[ $RANDOM % 100 ] >> $output_file 
	sleep 1
done
#---
