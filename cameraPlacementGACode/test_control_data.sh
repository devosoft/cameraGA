#!/bin/bash

# module rm Python/2.7.2
# module load Python/3.2.1

# control types 0 and 1 can have a number of cameras less than the desired because of the fixed grid 
# i = num control types
# j = number of replicates
# k = number of weeks of data 


num_cameras=$((60))
#func=$((2))
for ((func=0; func<4;func++)); do
  for ((i=0; i<2; i++)); do
    for ((j=0; j<30; j++)); do
        mkdir ../experimental_results/fit_func${func}/F104-F105
        mkdir ../experimental_results/fit_func${func}/F104-F105/control_tests
        mkdir ../experimental_results/fit_func${func}/F104-F105/control_tests/rep${j}
      for ((k=0; k<61; k++)); do
        wk2=$(($k+1))
        python3.2 testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/F104-F105/F104-F105_${k}_${k} -testSightingsData input/fieldData/hyenaData/F104-F105/F104-F105_${wk2}_${wk2} -camFile input/controlData/F104-F105/rep${j}/c_${i}_${k} -analysisOutFile ../experimental_results/fit_func${func}/F104-F105/control_tests/rep${j}/control_F104-F105_${i}_${k} -numCameras ${num_cameras}
      done
    done
  done


  for ((i=2; i<4; i++)); do
    for ((j=0; j<30; j++)); do
      for ((k=0; k<61; k++)); do
        wk2=$(($k+1))
        python3.2 testPlacedCameras.py -trainSightingsData input/fieldData/hyenaData/F104-F105/F104-F105_${k}_${k} -testSightingsData input/fieldData/hyenaData/F104-F105/F104-F105_${wk2}_${wk2} -camFile input/controlData/F104-F105/rep${j}/c_${i}_${k} -analysisOutFile ../experimental_results/fit_func${func}/F104-F105/control_tests/rep${j}/control_F104-F105_${i}_${k}
      done
    done
  done
done