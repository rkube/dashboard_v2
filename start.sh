#!/bin/bash

source /opt/conda/etc/profile.d/conda.sh
conda activate flask
export FLASK_ENV=development
python backend.py
