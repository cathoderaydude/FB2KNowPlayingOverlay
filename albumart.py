# Script for locating album art given a file path and copying it to
# the folder this script is run from.

# Created for use with https://github.com/cathoderaydude/FB2KNowPlayingOverlay
# but you could probably use this with other things, so feel free.

import sys
import os
import shutil 

# Make sure we were passed a filename
if len(sys.argv) < 2:
    exit()

# This is the folder passed on the command line
folder = sys.argv[1]

# Get the directory this script lives in so we know where
# to copy the file. Set the CWD as well, just to be safe.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Search for each likely filename
filenames = ["front.jpg", "cover.jpg", "folder.jpg", folder + ".jpg"]
for filename in filenames:
    if(os.path.exists(folder+'\\'+filename)):
        # Copy the file to this folder
        shutil.copyfile(folder+'\\'+filename, dname + "\\albumart.jpg")
        print (folder+'\\'+filename)
        print (dname + "\\albumart.jpg")
        exit() # We found it, bail
        
# If we made it here, no file was found, so sub in the placeholder
shutil.copyfile(dname + "\\noart.jpg", dname + "\\albumart.jpg")