#!/bin/bash


# scenario 0 only has 1 control b/c it is not stochastic (but create multiple anyway to ease testing by week)
# scenario 3 requires a file of locations to pull opportunistic locations from

# i = num control types
# j = number of replicates
# k = number of weeks of data 

for ((i=0; i<4; i++)); do
  for ((j=0; j<30; j++)); do
      mkdir M115/rep${j}
	for ((k=0; k<25; k++)); do
      python placeControlCams.py -s ${i} -o M115/rep${j}/c_${i}_${k} -l ../fieldData/hyenaData/M115/M115_${k}_${k}
	done;
  done;
done;

