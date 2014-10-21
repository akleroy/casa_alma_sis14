# This script steps through bandpass calibration, that is, the removal
# of frequency-dependent amplitude and phase effects. Before doing
# this, we solve for and remove some time dependent phase
# behavior. Then we apply the bandpass calibration to the data and see
# how to create a new, bandpass-calibrated data set.

# First, copy the data from the working directory
os.system("rm -rf sis14_twhya_uncalibrated.ms")
os.system("cp -r ../../working_data/sis14_twhya_uncalibrated.ms .")

# Run a listobs and note the bandpass calibrators. We have two, but
# will work with field 0 in this data set.
listobs("sis14_twhya_uncalibrated.ms")

# Gaincal is the general purpose task to solve for time-dependent
# amplitude and phase variations for each antenna. Here we carry out a
# short-timescale phase solution ("int") on the bandpass
# calibrator. This is saved as a calibration table "phase_int.cal".
os.system("rm -rf phase_int.cal")
gaincal(vis="sis14_twhya_uncalibrated.ms",
        caltable="phase_int.cal",
        field="0",
        solint="int",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Now we plot the calibration table, showing phase vs. time with a
# separate plot for each antenna. The two colors are the two
# correlations (i.e., polarizations).
plotcal(caltable="phase_int.cal",
        xaxis="time",
        yaxis="phase",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,-180,180])

# Now carry out a bandpass solution. This will solve for the amplitude
# and phase corrections needed for each channel for antenna. We use
# gaintable to feed the short-timescale phase solution to the
# task. This means that this table will be applied before the bandpass
# solution is carried out. We will deal with the overal normalization
# of the data later, for now we tell the task to solve for normalized
# (average=1) solutions via solnorm=True.

os.system("rm -rf bandpass.cal")
bandpass(vis="sis14_twhya_uncalibrated.ms",
         caltable="bandpass.cal",
         field="0",
         refant="DV22",
         solint="inf",
         combine="scan",
         solnorm=True,
         gaintable=["phase_int.cal"])

# We inspect the phase and amplitude behavior of the calibration
# plotting the corrections for each antenna using plotbandpass. We
# tell it to plot both phase and amplitude for three antennas at a
# time. Cycle through the plots.

plotbandpass(caltable="bandpass.cal",
        xaxis="chan",
        yaxis="both",
        subplot=32)

# Notice how noisy the solutions are. We can also calibrate the
# bandpass but average several channels at once, which is good if you
# think that signal-to-noise may be an issue and the solutions can be
# described as smoothly varying functions. We do this by setting a
# solution interval of 10 channels.

os.system("rm -rf bandpass_10chan.cal")
bandpass(vis="sis14_twhya_uncalibrated.ms",
         caltable="bandpass_10chan.cal",
         field="0",
         refant="DV22",
         solint="inf,10chan",
         combine="scan",
         solnorm=True,
         gaintable=["phase_int.cal"])

# Now plot these. There are less points and they are less noisy in
# absolute scale. Both tables seemed fine, but we will use these.

plotbandpass(caltable="bandpass_10chan.cal",
        xaxis="chan",
        yaxis="both",
        subplot=32)

# Apply the solutions - both in time and frequency - to the data using
# applycal. This creates a new corrected data column. Note that we
# will only apply these to field 0 at first and then look at the
# effects.

applycal(vis="sis14_twhya_uncalibrated.ms",
         field="0",
         gaintable=["bandpass_10chan.cal",
                    "phase_int.cal"],
         interp=["linear","linear"],
         gainfield=["0","0"])

# Plot the results of the calibration by comparing the dependence of
# phase and amplitude on channel before and after calibration.

plotms(vis="sis14_twhya_uncalibrated.ms",
       xaxis="chan",
       yaxis="phase",
       ydatacolumn="data",
       field="0",
       averagedata=T,
       avgtime="1e3",
       coloraxis="corr")

plotms(vis="sis14_twhya_uncalibrated.ms",
       xaxis="chan",
       yaxis="phase",
       ydatacolumn="corrected",
       field="0",
       averagedata=T,
       avgtime="1e3",
       coloraxis="corr")

plotms(vis="sis14_twhya_uncalibrated.ms",
       xaxis="chan",
       yaxis="amp",
       ydatacolumn="data",
       field="0",
       averagedata=T,
       avgtime="1e3",
       coloraxis="corr")

plotms(vis="sis14_twhya_uncalibrated.ms",
       xaxis="chan",
       yaxis="amp",
       ydatacolumn="corrected",
       field="0",
       averagedata=T,
       avgtime="1e3",
       coloraxis="corr")

# Now apply the bandpass solution to the whole data set. Note a couple
# things. First, this will overwrite the previous corrected data for
# the bandpass calibrator. Second, without the time-dependent gain
# factor applied the plotms plots above will not necessarily work as
# well (they do okay, but that's just lucky and good quality
# data). Instead, we now thing that we have removed frequency
# dependent effects from the whole data set and will proceed with a
# time-dependent calibration.

# Note that we use the non-standard "calonly" command, which tells
# applycal not to flag data for which the calibration has failed.

applycal(vis="sis14_twhya_uncalibrated.ms",
         field="",
         gaintable=["bandpass_10chan.cal"],
         interp=["linear"],
         gainfield=["0"],
         applymode="calonly")

# Now that we are satisfied with the bandpass calibration, we split
# out the bandpass calibrated data for further processing.

os.system("rm -rf sis14_twhya_bpcal.ms")
split(vis="sis14_twhya_uncalibrated.ms",
      datacolumn="corrected",
      outputvis="sis14_twhya_bpcal.ms",
      keepflags=False)

# This produces one of the supplied data products - so you can restart
# from a successful version of this script anytime.
