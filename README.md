# ChiaMover
script for moving completed plot files from temp directory tro final drive

# Usage
Modify the chaning watch_dir to the temp directory where your chia plots are being made

Also, add the destination drives/folders to dest_drives. These are should be in a format along the line of

dest_drives = [("/mnt/drive1", "label_drive1"), ("/mnt/drive2", "drive2"), ("/mnt/drive3", "drive3"), ("/mnt/drive4", "drive4")]

with /mnt/drive being the and "label_drive1" being a description of the diectory.

# Requirements
Python

# Notes
This script does not create plots. It just moves them after they are created. 
