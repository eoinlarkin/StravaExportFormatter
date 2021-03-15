#! python3

# The following code will unzip all the files in the strava directory
# and place in a new directory

# First we need to unzip the source file

import os
import zipfile
import re
import shutil
import gzip
import subprocess

content = os.listdir()
for filename in content:
    if filename.endswith('.zip') == False:
        content.remove(filename)

if len(content) > 1:
    print("More than one zip file in the directory")
else:
    print("Unzipping " + content[0])

with zipfile.ZipFile(content[0], 'r') as zip_ref:
    zip_ref.extractall("strava_download")

# Cleaning up the strava_download Folder
# Moving additional files to metadata folder
onlyfiles = [f for f in os.listdir("strava_download") if os.path.isfile(os.path.join("strava_download", f))]

# Moving to a new folder called metadata
os.mkdir("strava_download\metadata")
for f in onlyfiles:
    shutil.move(os.path.join("strava_download", f), os.path.join("strava_download\metadata", f))

# Creating a new directory for the unzipped activity files
shutil.copytree("strava_download\\activities", "strava_download\\activities_unzipped", symlinks=False, ignore=None)

# Unzipping all the files in the Unzipped folder and deleting the orignals
for file in os.listdir("strava_download\\activities_unzipped"):
     if file.endswith('.gz'):
         filepath = os.path.join("strava_download\\activities_unzipped", file)
         filepath_out = filepath.replace('.gz', '')
         with gzip.open(filepath, 'rb') as s_file, open(filepath_out, 'wb') as d_file:
             shutil.copyfileobj(s_file, d_file) 
        os.remove(filepath)
 
        
# Removing the whitespace from the tcx files:

filelist = os.listdir("strava_download\\activities_unzipped")
for filename in filelist:
    if filename.endswith('.tcx') == True:
        filepath = os.path.join("strava_download\\activities_unzipped", filename)
        file = open(filepath, encoding='utf-8')
        fileContents = file.read()
        fixed = re.sub(r'^\s+',"", fileContents).strip()
        file = open(filepath, "w", encoding='utf-8') # w command clears the file content
        file.write(fixed)

# Copying content to new folder for conversion to gpx
shutil.copytree("strava_download\\activities_unzipped", "strava_download\\activities_gpx", symlinks=False, ignore=None)

# Using gpsbabel to convert to gpx

def exec_cmd(command):
    result = subprocess.Popen(command, shell=True)
    text = result.communicate()[0]
    return_code = result.returncode
    if return_code != 0:
        return False
    return True

# gpsbabel command, expecting to be in PATH. You may put the absolute path to the executable (mostly for Windows users)
gpsbabel_switch_tcx = "gpsbabel -t -i gtrnctr -f {filepath_tcx} -o gpx -F {filepath_gpx}"
gpsbabel_switch_fit = "gpsbabel -t -i garmin_fit -f {filepath_fit} -o gpx -F {filepath_gpx}"

filelist = os.listdir("strava_download\\activities_gpx")

for filename in filelist:
    if filename.endswith('.tcx') == True:
        filepath_tcx = os.path.join("strava_download\\activities_gpx", filename)
        filepath_gpx = filepath_tcx.replace(".tcx", ".gpx")
        rc = exec_cmd(gpsbabel_switch_tcx.format(filepath_gpx=filepath_gpx, filepath_tcx=filepath_tcx))
        if rc: os.remove(filepath_tcx)
    
    if filename.endswith('.fit') == True:
        filepath_fit = os.path.join("strava_download\\activities_gpx", filename)
        filepath_gpx = filepath_fit.replace(".fit", ".gpx")
        rc = exec_cmd(gpsbabel_switch_fit.format(filepath_gpx=filepath_gpx, filepath_fit=filepath_fit))
        if rc: os.remove(filepath_fit)

filelist        
filepath_tcx = os.path.join("strava_download\\activities_gpx", filename)
print(filepath_gpx)

print(filelist)
