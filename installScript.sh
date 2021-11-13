#!/bin/bash
sudo echo 'Moving usr/bin/shazam to /usr/bin...'
sudo cp usr/bin/shazam /usr/bin/
echo 'Moving usr/lib/shazam usr/lib/...'
sudo cp usr/lib/shazam  -r /usr/lib/
echo 'Done!'
