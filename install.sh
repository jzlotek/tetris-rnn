#!/bin/bash
#
# Author: Joseph Hines
#
# 04/09/19
#

if [[ -d venv/bin ]]; then
  source venv/bin/activate
else
  echo "VENV not found. Installing..."
  virtualenv -p python3 ./venv
  source venv/bin/activate
fi

if [[ -f ./requirements.txt ]]; then
  pip install -r requirements.txt
fi

echo "VENV found."
