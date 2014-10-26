# This script steps through some very common operations that you would
# use to get oriented with a new data set.

# First, copy the data from the working directory
os.system("rm -rf sis14_twhya_uncalibrated.ms")
os.system("cp -r ../working_data/sis14_twhya_uncalibrated.ms .")

# List the contents of the observations - here they will appear in the
# log, but you can also shunt them to a text file using the listfile
# option. Look at the output to see the sequence of observations, the
# intent of each observation, the set of spectral windows, and the
# lists of fields and sources.
listobs("sis14_twhya_uncalibrated.ms")

# Plot the locations of the antennas. By default this will show them
# in a window on the screen. Here we tell it to make a .PNG file and
# then run a command to open that file.
plotants("sis14_twhya_uncalibrated.ms", figfile="plotants.png")
os.system("xv plotants.png")

# Pick a reference antenna. DV22 is fairly central without being
# clearly shadowed and we don't find anything wrong with it later in
# the calibration. That will serve as our "refant" (reference antenna)
# throughout the guide based on this plot.

# Now we will try to get a basic idea of the observing plan. We will
# use "plotms", the general purpose plotting task for CASA visibility
# data. First, examine the inputs using

inp plotms

# But don't worry, there's a very nice GUI.

# We use plotms to look at amplitude vs. time (remember that right now
# the data are uncalibrated). We color by field and average together
# all the spectral channels. At the same time run listobs and compare
# to the output to get a sense of the observing strategy.

plotms(vis="sis14_twhya_uncalibrated.ms", xaxis="time", yaxis="amp",
       averagedata=T, avgchannel="1e3", coloraxis="field")

listobs("sis14_twhya_uncalibrated.ms")

# Another basic orientation plot is the u-v coverage. Remember that
# this sets the spatial scales to which you are sensitive. Plot the
# u-v coverage for each field using plotms.

plotms(vis="sis14_twhya_uncalibrated.ms", xaxis="u", yaxis="v",
       averagedata=T, avgchannel="1e3", coloraxis="field")
