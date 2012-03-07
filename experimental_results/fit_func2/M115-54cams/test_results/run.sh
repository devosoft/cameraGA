#!/bin/bash

module rm Python/2.7.2
module load Python/3.2.1


for ((i=0; i<24; i++)); do
	j=$(($i+1))
	python ui.py -s ${1} -bestOutput output/M115/ga_${i} -sightingsData input/fieldData/hyenaData/M115/M115_${i}_${i}
	python testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/M115/M115_${i}_${i} -testSightingsData input/fieldData/hyenaData/M115/M115_${j}_${j} -camFile output/M115/ga_${i} -analysisOutFile output/res/res_M115_${i}_${j}

done

