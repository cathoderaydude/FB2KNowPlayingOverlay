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

# This is the file passed on the command line
file = sys.argv[1]
# Get the path to the file
folder = os.path.dirname(file)
# And get the folder name for the file
foldername = os.path.basename(folder)

print ("file" + file)
print ("folder" + folder)
print ("foldername " + foldername)

# Get the directory this script lives in so we know where
# to copy the file. Set the CWD as well, just to be safe.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# First, try TinyTag - if present
try:
    from tinytag import TinyTag
    from PIL import Image
    import io
    
    # Try to parse file
    tag = TinyTag.get(file, image=True)
    # Look for cover art
    if tag.images is not None and tag.images.front_cover is not None:
        # There is, supposedly, cover art in the file.
        # PIL should convert it to jpeg automatically, so format doesn't matter
        Image.open(io.BytesIO(tag.images.front_cover.data)).save("albumart.jpg")
        
        # And since we succeeded, go ahead and exit
        exit()
except ImportError as e:
    # If we failed to import a library, tell the user in case they're debugging
    print ("Error importing library: " + str(e))
except Exception as e:
    # If pretty much anything else goes wrong we just want to bail and try to use a file instead.
    print ("Error trying to use TinyTag: " + str(e))

# Search for each likely filename
filenames = ["front.jpg", "cover.jpg", "folder.jpg", os.path.dirname(foldername) + ".jpg"]
for filename in filenames:
    if(os.path.exists(folder+'\\'+filename)):
        # Copy the file to this folder
        shutil.copyfile(folder+'\\'+filename, dname + "\\albumart.jpg")
        print (folder+'\\'+filename)
        print (dname + "\\albumart.jpg")
        exit() # We found it, bail
        
# If we made it here, no file was found, so sub in the placeholder
shutil.copyfile(dname + "\\noart.jpg", dname + "\\albumart.jpg")