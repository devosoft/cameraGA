#!/bin/bash

# module rm Python/2.7.2
# module load Python/3.2.1

# control types 0 and 1 can have a number of cameras less than the desired because of the fixed grid 
# i = num control types
# j = number of replicates
# k = number of weeks of data 


num_cameras=$((39))
#func=$((0))
for ((func=0; func<4;func++)); do
  for ((i=0; i<2; i++)); do
    for ((j=0; j<30; j++)); do
        mkdir ../experimental_results/fit_func${func}/west
        mkdir ../experimental_results/fit_func${func}/west/control_tests
        mkdir ../experimental_results/fit_func${func}/west/control_tests/rep${j}
      for ((k=0; k<22; k++)); do
        wk2=$(($k+1))
        python3.2 testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/west/west_${k}_${k} -testSightingsData input/fieldData/hyenaData/west/west_${wk2}_${wk2} -camFile input/controlData/west/rep${j}/c_${i}_${k} -analysisOutFile ../experimental_results/fit_func${func}/west/control_tests/rep${j}/control_west_${i}_${k} -numCameras ${num_cameras} -func ${func}
      done
    done
  done


for ((i=2; i<4; i++)); do
  for ((j=0; j<30; j++)); do
    for ((k=0; k<22; k++)); do
      wk2=$(($k+1))
      python3.2 testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/west/west_${k}_${k} -testSightingsData input/fieldData/hyenaData/west/west_${wk2}_${wk2} -camFile input/controlData/west/rep${j}/c_${i}_${k} -analysisOutFile ../experimental_results/fit_func${func}/west/control_tests/rep${j}/control_west_${i}_${k} -func ${func}
      done
   done
 done
done