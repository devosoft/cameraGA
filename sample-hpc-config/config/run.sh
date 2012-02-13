#!/bin/bash

module rm Python/2.7.2
module load Python/3.2.1


python ui.py -s ${1}
python testPlacedCameras.py
