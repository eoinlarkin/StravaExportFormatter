# StravaExportFormatter
Simple Python script for automation of the clean-up of Strava's Export Your Data feature.

## Background
[Strava](https://www.strava.com) is a social network for the tracking and analysing of online activities. It is mostly used for cycling and running with activities recorded using both gps and non-gps enabled devices. 

Strava is device agnostic and for many individuals it is their main reference for activity history hence the expression *[if it's not on Strava it didn't happen](https://www.bicycling.com/culture/a22736718/why-strava-and-instagram-are-so-addicting-for-cyclists/)*.

Activity files are generally *.xml* based, however depending on the format and generation of the device the file format can differ. For instance, Older Garmin devices use the *.tcx* file format, while newer Garmin and Wahoo devices record in *.fit* format. 

To complicate matters, the *.gpx* format is the best supported activity file format and the most useful for use with external tools. However, converting files individually to this format can be tedious for a large number of files. 

An example of the added functionality is the following plot of individual activities which was generated using R and the `Strava` [package](https://github.com/marcusvolz/strava)

![](/plots/facets_plot-1.png)

## Motivation
Given Strava's ability for digesting multiple file types from different devices, being able to bulk export all data for analysis is a key feature. Strava provides [functionality for this](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export), however the export provided is a bit of a mess.

- The activity files in the data extract is in *.gzip* format and need to be individually unzipped
- The data is poorly structured with a large number of files dumped into a single folder
- Strava's implementation of *.tcx*  is not fully compliant and the files are incompatible with conversion tools such as GPSBabel. This is a [known issue](https://github.com/gpsbabel/gpsbabel/issues/371)
- Files in the Bulk Export are in the individual upload format; there is no version to download *.gpx* versions of the activity files.

## Process
The script performs the following steps:

- Strava export file is unzipped for processing
- Activity files are unzipped
- Malformed *.tcx* files are fixed using regex
- Files are converted to *.gpx* format using [GPSBabel](https://www.gpsbabel.org/)

## Running the Script
In order to run the script, complete the following steps:

- Download your data from Strava using their *Export Your Data* tool:[link](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export)
- Place the downloaded *.zip* file in a folder with the Python script
- Execute the script using Python in the folder e.g. `python StravaExportFomratter.py`
- Follow the prompts as the script executes

Script has been tested on **Python 3.8** on a Windows PC. 

## Future Functionality
Future enhancements to include:

- Renaming of activity files to a more friendly format based on dates
- Generate plots as part of the clean-up providing summary information of the activities





