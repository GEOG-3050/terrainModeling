# Name: 
# Description: 
# 
# Requirements: Spatial Analyst Extension
# Import system modules

import arcpy
from arcpy import env
from arcpy.sa import *

# Create a Triangular Irregular Network (TIN) model of the terrain #####################
arcpy.env.workspace = r"E:/GitHub/terrainModeling/chp12data.gdb"

"""
	DEM to TIN
	The TIN data cannot be saved in a geodatabase, so the output data
	should be put into a folder e.g. E:/GitHub/terrainModeling/chp12data.gdb/tin
"""
arcpy.RasterTin_3d("dem", "tin") 

"""
	TIN to DEM
	The cell size of the new DEM is 50 meters, values are in the 
	float type, and the methos used to raster the DEM is linear
	interpolation 
"""
arcpy.TinRaster_3d(in_tin=r"chp12data.gdb/tin", out_raster="demFromTIN", \
                   data_type="FLOAT", method="LINEAR", \
                   sample_distance="CELLSIZE 50",z_factor="1")

# Create contour lines ##################################################################
"""
	The input is "dem" and the output is "contour".
	The contour is in 10 meter intervals and starts from 330 meters.
"""
arcpy.Contour_3d(in_raster="dem", out_polyline_features=" contour", \
                 contour_interval="10", base_contour="330", z_factor="1")

# Create slope raster ###################################################################
# the input is DEM, and slope is in the unit of degrees
slopely = arcpy.sa.Slope("dem", "DEGREE")
# save the slope layer into geodatabase (path has been set above)
slopely.save("slope")

# Create aspect raster ##################################################################
aspectly = arcpy.sa.Aspect("dem")
aspectly.save("aspect")

# Create flow direction raster ##########################################################
"""
	Create flow direction with "dem" as input.  The "NORMAL" argument means
	edge cells are not forced outward, but follow normal flow rules.
"""
fd = arcpy.sa.FlowDirection("dem","NORMAL")

# Calculate sinks in DEM ################################################################
sinks = arcpy.sa.Sink("fd")
# fill the sinks on dem
dem_sinkfilled = arcpy.sa.Fill("dem")

# Calculate flow accumulation ##########################################################
# recreate flow direction on the dem with sinks filled
fd_filled = arcpy.sa.FlowDirection("dem_sinkfilled","NORMAL")
# calculate the flow accumulation
fa = arcpy.sa.FlowAccumulation("fd_filled","","INTEGER")
