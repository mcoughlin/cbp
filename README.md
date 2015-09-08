# cbp
Scripts for running the collimated beam projector and analyzing output

Every instrument (the zaber sliders, focuser, filter wheel, etc. has its own script for control).

As an example, for a raster in X-Y with a grid of 130:10:150 by 50:20:100.
python raster.py --doRaster --rasterType XY --xmin 130.0 --xmax 150.0 --dx 10.0 --ymin 50.0 --ymax 100.0 --dy 20.0

Filter Wheel:
There are 10 slots in the filter wheel, 5 dedicated to masks and 5 dedicated to filters. These can be found in masks.txt and filters.txt respectively.

