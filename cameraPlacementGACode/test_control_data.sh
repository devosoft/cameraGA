#!/bin/bash

# module rm Python/2.7.2
# module load Python/3.2.1

# control types 0 and 1 can have a number of cameras less than the desired because of the fixed grid 
# i = num control types
# j = number of replicates
# k = number of weeks of data 


num_cameras=$((45))
func=$((2))
#for ((func=0; func<4;func++)); do
  for ((i=0; i<2; i++)); do
    for ((j=0; j<30; j++)); do
        mkdir ../experimental_results/fit_func${func}/M115
        mkdir ../experimental_results/fit_func${func}/M115/control_tests
        mkdir ../experimental_results/fit_func${func}/M115/control_tests/rep${j}
      for ((k=0; k<24; k++)); do
        wk2=$(($k+1))
        python3.2 testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/M115/M115_${k}_${k} -testSightingsData input/fieldData/hyenaData/M115/M115_${wk2}_${wk2} -camFile input/controlData/M115/rep${j}/c_${i}_${k} -analysisOutFile ../experimental_results/fit_func${func}/M115/control_tests/rep${j}/control_M115_${i}_${k} -numCameras ${num_cameras} -func ${func}
      done
    done
  done


  for ((i=2; i<4; i++)); do
    for ((j=0; j<30; j++)); do
      for ((k=0; k<24; k++)); do
        wk2=$(($k+1))
        python3.2 testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/M115/M115_${k}_${k} -testSightingsData input/fieldData/hyenaData/M115/M115_${wk2}_${wk2} -camFile input/controlData/M115/rep${j}/c_${i}_${k} -analysisOutFile ../experimental_results/fit_func${func}/M115/control_tests/rep${j}/control_M115_${i}_${k} -func ${func}
      done
    done
  done
#done