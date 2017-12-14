#!/bin/bash

apt-get install python3
apt-get install python3-pip
pip3 install click
pip3 install urllib

chmod +x ./camllight_interpreter
cp ./camllight_interpreter /usr/bin/

echo "Installation was successful!"
