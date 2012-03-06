#!/bin/bash


# scenario 0 only has 1 control b/c it is not stochastic (but create multiple anyway to ease testing by week)
# scenario 3 requires a file of locations to pull opportunistic locations from

# i = num control types
# j = number of replicates
# k = number of weeks of data 

for ((i=0; i<4; i++)); do
  for ((j=0; j<30; j++)); do
      mkdir M114
      mkdir M114/rep${j}
	for ((k=0; k<2; k++)); do
      python placeControlCams.py -s ${i} -o M114/rep${j}/c_${i}_${k} -l ../fieldData/hyenaData/M114/M114_${k}_${k}
	done;
  done;
done;

