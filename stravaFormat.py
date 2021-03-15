#! python3


import os
import re
# import subprocess
# import csv
# import sys


folder = "C:\\Users\\Eoin\\OneDrive\\Data Science\\Projects\\Strava Download Formatter" 
filename = "54675694.tcx"

filepath = os.path.join(folder, filename)
print(filepath)

filepath_test = os.path.join(folder, "test.tcx")
filepath_test_orig = os.path.join(folder, "test_github_version.tcx")

file = open(filepath, encoding='utf-8')
content = file.read()

fixed = re.sub(r'^\s+',"", content).strip()

# print(fixed)

filew = open(filepath_test, "w", encoding='utf-8') 
filew.write(fixed)

fixed = re.sub(r'>\s\s+<', '><', content).strip()
filew = open(filepath_test_orig, "w", encoding='utf-8') 
filew.write(fixed)

# extension = os.path.splitext(filename)[1][1:].strip().lower()
# print(filename.ljust(40," ") + "| " + line["type"].ljust(13," ") + "| " + str(line["name"])[:70])

#  # strip spaces from tcx
# if extension == "tcx":
#     with open(filename, encoding='utf-8') as file:
#         content = file.read()
#         fixed = re.sub(r'>\s\s+<', '><', content).strip()
#         with open(filename, "w", encoding='utf-8') as filew:
#             filew.write(fixed)
#             print(re.findall(r'<[Aa][Cc][Tt][Ii][Vv][Ii][Tt][Yy][ ]{1,}[Ss][Pp][Oo][Rr][Tt]="([^"]*)">', fixed))