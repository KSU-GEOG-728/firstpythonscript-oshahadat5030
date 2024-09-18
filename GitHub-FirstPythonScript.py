#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    File name: GitHub-FirstPythonScript.py
    Author: Shahadat Hossain
    Description:  First Python script. This script selects the Flint Hills ecoregion, buffers it,
    clips major rivers within the buffered region, and calculates the total length of the streams in miles
    Date created: 9/17/2024
    Python Version: 3.9.16
"""

# Import arcpy module and allow overwrites
import arcpy
arcpy.env.overwriteOutput = True

# Set current workspace
arcpy.env.workspace = "D:\\Fall 24\\Geog 728\\GitHub-FirstPythonScript\\GitHub-FirstPythonScript.gdb"


#perform geoprocessing

#Step 1: Buffer the Flint Hills ecoregion by 10 kilometers
#Need to save result as a result object otherwise the all ecoregions will be buffered in the next line
selectRegion = arcpy.management.SelectLayerByAttribute('ks_ecoregions', 'NEW_SELECTION', "US_L3NAME ='Flint Hills' ")
arcpy.analysis.Buffer(selectRegion, 'outBuff', '10 kilometers')

# Step 2: Clip major rivers in Kansas using the buffered boundary
arcpy.analysis.Clip('ks_major_rivers', 'outBuff', 'outClip')

# Step-3: Add a new field to store stream lengths in miles
# Missing quotation marks around outClip - this is a dataset and not a variable
arcpy.management.AddField('outClip', 'StreamLengthMiles', 'DOUBLE')
arcpy.management.CalculateGeometryAttributes(
    'outClip',
    [['StreamLengthMiles', 'LENGTH']],
    length_unit='MILES_US'  
)

# Step 4: Summarize total stream length 
total_length = 0
with arcpy.da.SearchCursor('outClip', ['StreamLengthMiles']) as cursor:
    for row in cursor:
        total_length += row[0]

# Step 5: Output the total length of streams
print(f'Total stream length in the buffered region: {total_length:.2f} miles')
