#!/bin/bash


# scenario 0 only has 1 control b/c it is not stochastic
python placeControlCams.py -s 0 -o controlPlacements/c_0

for ((i=1; i<3; i++)); do
	for ((j=0; j<30; j++)); do
		python placeControlCams.py -s ${i} -o controlPlacements/c_${i}_${j}	
	done;
done;

