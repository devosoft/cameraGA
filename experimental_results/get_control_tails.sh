#!/bin/bash

# i = num control types
# j = number of replicates
# k = number of weeks of data 

mkdir M115/control_results
for ((i=0;i<4;i++)); do
  for ((j=0;j<30;j++)); do
    for ((k=0;k<24;k++)); do
      tail -n 1 M115/control_tests/rep${j}/control_M115_${i}_${k} >> M115/control_results/control_${i}_wk${k}.dat
      echo >> M115/control_results/control_${i}_wk${k}.dat
    done
  done
done
