#! python3

# Importing required libraries
import os
import zipfile
import re
import shutil
import gzip
import subprocess
import glob

# ********************************************************************
# Function to print a progress bar for iterations
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
# ********************************************************************
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

# ********************************************************************
# Function to validate user input
# An input message is passed to the function, output returned is either yes or no
# ********************************************************************
def request_YesNo(InputMsg):
    while True:
        print(InputMsg)
        usrOutput = input()
        while usrOutput.lower() not in ("yes", "no"):
            usrOutput = input("Input not valid. Please enter either Yes or No:")
        else:
            return usrOutput.lower() # coverting output to lower case

# ********************************************************************
# Function to call .exe files - used to execute GPSBabel
# ********************************************************************
def exec_cmd(command):
    result = subprocess.Popen(command, shell=True)
    text = result.communicate()[0]
    return_code = result.returncode
    if return_code != 0:
        return False
    return True

# ********************************************************************
# Stage 01
# Unzipping the Strava Export File
# ********************************************************************

filelist = glob.glob("*.zip")

if len(filelist) > 1:
    print("There is more than one zip file in the directory. \n Ensure that the Strava Export zip file is in the directory and try again.")
    exit()
else:
    print('\n' + '*' * 75 + "\n Unzipping " + filelist[0])

# Extracting the Strava Zip file using the progressBar function to indicate progress
with zipfile.ZipFile(filelist[0]) as zf:
    for member in progressBar(zf.infolist(), prefix = 'Progress:', suffix = 'Complete', length = 50):
        try:
            zf.extract(member, path="strava_download")
        except zipfile.error as e:
            pass

# ********************************************************************
# Stage 02
# Cleaning up the strava_download Folder
# ********************************************************************

# Getting list of files in the unzipped directory
onlyfiles = [f for f in os.listdir("strava_download") if os.path.isfile(os.path.join("strava_download", f))]

# Moving to a new folder called metadata
print('\n' + '*' * 75 + "\n Moving non activity files to metadata folder:")
os.mkdir("strava_download\metadata")
for f in onlyfiles:
    shutil.move(os.path.join("strava_download", f), os.path.join("strava_download\metadata", f))

# Creating a new directory for the unzipped activity files
print('\n' + '*' * 75 + "\n Creating a new directory for the unzipped activty files:")
shutil.copytree("strava_download\\activities", "strava_download\\activities_unzipped", symlinks=False, ignore=None)

# Unzipping all the files in the Unzipped folder and deleting the orignals
print('\n' + '*' * 75 + "\n Unzippling the Activity files:")

filelist = os.listdir("strava_download\\activities_unzipped")
for file in progressBar(filelist, prefix = 'Progress:', suffix = 'Complete', length = 50):
     if file.endswith('.gz'):
         filepath = os.path.join("strava_download\\activities_unzipped", file)
         filepath_out = filepath.replace('.gz', '')
         with gzip.open(filepath, 'rb') as s_file, open(filepath_out, 'wb') as d_file:
             shutil.copyfileobj(s_file, d_file) 
         os.remove(filepath)
 
# Checking whether to delete the activities folder
delDirectory = request_YesNo('\n' + '*' * 75 + '\n Would you like to delete the activites folder?')
if delDirectory == "yes":
    print("Deleting Activities folder")
    shutil.rmtree("strava_download\\activities")


# ********************************************************************
# Stage 03
# Reformatting the Tcx files
# ********************************************************************

# Removing the whitespace from the tcx files:
print('\n' + '*' * 75 + '\n Correcting the formatting for .tcx files')

# Getting the list of files in hte folder
filelist = os.listdir("strava_download\\activities_unzipped")

# Removing the leading whitespace from tcx files
for filename in progressBar(filelist, prefix = 'Progress:', suffix = 'Complete', length = 50):
    if filename.endswith('.tcx') == True:
        filepath = os.path.join("strava_download\\activities_unzipped", filename)
        file = open(filepath, encoding='utf-8')
        fileContents = file.read()
        fixed = re.sub(r'^\s+',"", fileContents).strip()
        file = open(filepath, "w", encoding='utf-8') # w command clears the file content
        file.write(fixed)
        file.close()

# ********************************************************************
# Stage 04
# Converting files to gpx format
# ********************************************************************

usrInput = request_YesNo('\n' + '*' * 75 + '\n Would you like to convert the activity files to .gpx format ? \n Enter Yes or No:')
if usrInput == "yes":
    print("\n Converting the files to gpx using GPSBabel")

    # Copying content to new folder for conversion to gpx
    shutil.copytree("strava_download\\activities_unzipped", "strava_download\\activities_gpx", symlinks=False, ignore=None)

    # Updating user on progress
    print('\n' + '*' * 75 + "\n Converting the files to gpx using GPSBabel:")

    # gpsbabel command, expecting to be in PATH. You may put the absolute path to the executable (mostly for Windows users)
    gpsbabel_switch_tcx = "gpsbabel -t -i gtrnctr -f {filepath_tcx} -o gpx -F {filepath_gpx}"
    gpsbabel_switch_fit = "gpsbabel -t -i garmin_fit -f {filepath_fit} -o gpx -F {filepath_gpx}"
    filelist = os.listdir("strava_download\\activities_gpx")

    fit_counter, tcx_counter, gpx_counter = 0, 0, 0
    for filename in progressBar(filelist, prefix = 'Progress:', suffix = 'Complete', length = 50):

        if filename.endswith('.gpx') == True: gpx_counter += 1

        if filename.endswith('.tcx') == True:
            filepath_tcx = os.path.join("strava_download\\activities_gpx", filename)
            filepath_gpx = filepath_tcx.replace(".tcx", ".gpx")
            rc = exec_cmd(gpsbabel_switch_tcx.format(filepath_gpx=filepath_gpx, filepath_tcx=filepath_tcx))
            if rc: 
                tcx_counter += 1
                os.remove(filepath_tcx)
        
        if filename.endswith('.fit') == True:
            filepath_fit = os.path.join("strava_download\\activities_gpx", filename)
            filepath_gpx = filepath_fit.replace(".fit", ".gpx")
            rc = exec_cmd(gpsbabel_switch_fit.format(filepath_gpx=filepath_gpx, filepath_fit=filepath_fit))
            if rc: 
                fit_counter += 1
                os.remove(filepath_fit)

    # Checking whether to delete the unzipped activities folder
    # This contains the activity files in the original file formats
    usrInput = request_YesNo('\n' + '*' * 75 + "\n Would you like to delete the 'activities_unzipped' folder? \n Enter Yes or No:")
    if usrInput == "yes":
        print("Deleting 'activites_unzipped' folder")
        shutil.rmtree("strava_download\\activities_unzipped")

# ********************************************************************
# To Do 
# Rename files to reference the date of activity
# ********************************************************************

# Summarising the output
print('*' * 50)
print("Conversion completed. \n" + str(fit_counter) + \
    " files converted from .fit format to .gpx \n" + str(tcx_counter) + \
    " files converted from .tcx format to .gpx \n" \
        "Total number of gpx files: " + str(fit_counter + tcx_counter + gpx_counter))


