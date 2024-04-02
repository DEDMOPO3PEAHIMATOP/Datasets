#!/bin/bash
sudo apt-get install python3-tk
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
python3 main.py
read
