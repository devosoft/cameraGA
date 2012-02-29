#!/bin/bash


# scenario 0 only has 1 control b/c it is not stochastic (but create multiple anyway to ease testing by week)
# scenario 3 requires a file of locations to pull opportunistic locations from

for ((i=0; i<4; i++)); do
	for ((j=0; j<30; j++)); do
      python placeControlCams.py -s ${i} -o M115/c_${i}_${j}	-l ../fieldData/hyenaData/M115/M115_${j}_${j}
	done;
done;

