Modular tutorials for ALMA/CASA
-------------------------------

These tutorials step through an introduction to the key parts of reducing
an ALMA data set in CASA. They go through the whole prcedure of inspecting,
calibrating, and then imaging a real PI ALMA data set (published in Qi, Oberg 
et al. 2013) looking at the nearby star TW Hydra.

The scripts are modularized, so that if you are interested only in one part
the provided data allow you to work through only that tutorial. For example,
if you are only interested in getting an introduction to imaging, you 
can  focus on the imaging and line_imaging tutorials and then expand
into the moments and selfcal tutorials as you prefer. 

Getting the Data
----------------

The script package (which you have here) is small and can be help in a
repository (just grab the tarball from the right hand part of the page). 
The data are too big to be easily checked in here and so are served off the 
NRAO web page. The final location is TBD but for now the targball is at:

ftp://ftp.cv.nrao.edu/NRAO-staff/aleroy/tutorial_data.tar.gz

All of the tutorials should live in a parent directory (this repository hosts
the directory setup). Just move the tarball of the data into this directory and untar
it. The data should be unpacked into the working_data directory. 

CASA Basics
-----------

* first_task: Run your first CASA task and see how scripts are run.

* orient: Orient yourself when working with visibility data, plotting
  antenna positions, inspecting the data, etc.

Calibration
-----------

These tutorials step you through basic calibration and data
inspection.

* bandpass - "Bandpass calibration" : step through how to calibrate the frequency-dependent amplitude and phase response of the telescope.

* gaincal - "Phase and amplitude calibration" : step through how to calibrated the time-dependent amplitude and phase response of the telescope.

* inspection - "Data inspection and flagging." : step through the basics of inspecting data and identifying bad data.

* end_to_end - "End to end (iterative) calibration" : work through a real complete calibration and see how you might merge visual inspection with scripting.

Imaging
-------

* imaging - "Basic imaging" : work through basic continuum imaging of calibrated data.

* selfcal - "Self calibration" : work through the basics of applying iterative phase and amplitude self calibration.

* line_imaging - "Continuum Subtraction and Line imaging" : work through how to image a line data cube.

* moments - "Moment creation and basic analysis" : see how to use CASA to perform some basic data analysis.

