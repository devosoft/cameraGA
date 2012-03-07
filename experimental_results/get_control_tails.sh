#!/bin/bash

# i = num control types
# j = number of replicates
# k = number of weeks of data 
# l = fitness function

mkdir control_results/M115
l=0
mkdir control_results/M115/fit_func${l}
for ((i=0;i<4;i++)); do
  for ((j=0;j<30;j++)); do
    for ((k=0;k<24;k++)); do
      tail -n 1 fit_func${l}/M115/control_tests/rep${j}/control_M115_${i}_${k} >> control_results/M115/fit_func${l}/control_${i}_wk${k}.dat
      echo >> control_results/M115/fit_func${l}/control_${i}_wk${k}.dat
    done
  done
done
