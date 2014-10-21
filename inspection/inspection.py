# The script steps through the basics of data inspection and
# flagging. Throughout the calibration process you will want to create
# a series of diagnostic plots and use these to identify and remove
# problematic data. This lesson steps through common steps in
# identifying and flagging problematic data. In the next lesson, we
# will see how this interplays with calibration in a typical iterative
# workflow.


# First copy the calibrated (but not flagged) data
os.system("rm -rf sis14_twhya_calibrated.ms")
os.system("cp -r ../working_data/sis14_twhya_calibrated.ms .")

# Re-orient yourself if necessary
listobs("sis14_twhya_calibrated.ms")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Inspect your data
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# We will now use plotms to make a series of diagnostic plots. These
# plots have been picked because we have a good expectation of what
# the calibrators (fields 0, 2, and 3 here) should look like in each
# space. In general, we will look through these plots one at a time
# and look for data that appears as outliers. Use the "locate"
# function, manipulate the plotted axes, and change the data selection
# and averaging to try to identify the minimum way to specify the
# problem data (antenna, scan, channel, etc.). Keep in mind here that
# the *science* data are not generally show and will still need to be
# flagged.

# Start with plots of amplitude and phase vs. uv distance. For point
# sources we expect flat amplitude and zero phases for these plots.

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="uvdist",
       yaxis="amp",
       ydatacolumn="corrected",
       field="0,2,3",
       averagedata=T,
       avgchannel="1e3",
       avgtime="1e3",
       iteraxis="field",
       coloraxis="corr")

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="uvdist",
       yaxis="phase",
       ydatacolumn="corrected",
       field="0,2,3",
       averagedata=T,
       avgchannel="1e3",
       avgtime="1e3",
       iteraxis="field",
       coloraxis="corr")

# We see some outliers. Using "locate" we clearly see that DV19 is
# having problems for the bandpass calibrator, showing low
# amplitudes. Let's have a look at amplitude vs. time.

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="time",
       yaxis="amp",
       ydatacolumn="corrected",
       field="0,2,3",
       averagedata=T,
       avgchannel="1e3",
       coloraxis="field")

# Again, you see the same issues. We'll note that we want to flag
# DV19. Potentially we could flag it only on field 0, it's not totally
# clear that it's bad throughout the track. However, this means we
# will need to come up with an alternative calibration scheme for the
# bandpass (possibly using the other quasar). We will plan to flag
# DV19.

# Next we will inspect phase and amplitude as a function of
# antenna. Each visibility (point) has two antennas associated with
# it, which are identified as Antenna1 and Antenna2 based on their
# number (the lower number is always 1). Remember here that we don't
# expect astrophysical signals to show up strongly as a function of
# antenna unless the antenna sits in a very unsual point in the array
# (check your plotants).

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="antenna1",
       yaxis="amp",
       ydatacolumn="corrected",
       field="0,2,3",
       iteraxis="field",
       averagedata=T,
       avgchannel="1e3",
       avgtime="1e3")

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="antenna2",
       yaxis="amp",
       ydatacolumn="corrected",
       field="0,2,3",
       iteraxis="field",
       averagedata=T,
       avgchannel="1e3",
       avgtime="1e3")

# You can see the problems with DV19 on field 0 here and you can also
# notice that DV01 has low amplitudes on field 3 (all amplitudes are
# low for this antenna). You may also notice that DV20 (antennae 22)
# shows some (but not all) low amplitudes, mostly on scan 30. We will
# note this and also plan to flag DV01.

# Now look at the same plot in phase.

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="antenna1",
       yaxis="phase",
       ydatacolumn="corrected",
       field="0,2,3",
       iteraxis="field",
       averagedata=T,
       avgchannel="1e2",
       avgtime="1e3")

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="antenna2",
       yaxis="phase",
       ydatacolumn="corrected",
       field="0,2,3",
       iteraxis="field",
       averagedata=T,
       avgchannel="1e2",
       avgtime="1e3")

# The issue with DV 22 is particularly evident in these phase plots on
# Field 3, especially looking at Antennae2 (because 22 is a high
# number it's more commonly found as Antennae2).

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="scan",
       yaxis="phase",
       ydatacolumn="data",
       field="3",
       antenna="",
       averagedata=T,
       avgchannel="1e6",
       iteraxis="field",
       coloraxis="corr",
       avgtime="1e6",
       avgscan=False)

# You can see that likely DV19 is only really problematic in the first
# part of the track. Later on, scans 26 ~ 34, we see issues with DV20
# (Antenna 22). We will plan to flag DV 20 over that range.

# Finally, we don't expect strong lines in the calibrators and sharp,
# unexpected spikes anywhere are likely to be spurious. We will likely
# want to flag any lines or spikes. Plot the amplitude and phase as a
# function of channel for the calibrators.

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="channel",
       yaxis="amp",
       ydatacolumn="corrected",
       field="0,2,3",
       averagedata=T,
       avgtime="1e6",
       iteraxis="field",
       avgscan=True)

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="channel",
       yaxis="phase",
       ydatacolumn="corrected",
       field="0,2,3",
       averagedata=T,
       avgtime="1e6",
       avgchannel="10",
       iteraxis="field",
       avgscan=True)

# Field 2 (Ceres) shows an unexpected spike around channel 130. That
# seems spurious and we will want to flag this channel range.

# Finally, one can look at the continuity of the phase vs. time for
# each antenna paired with the reference. This is a good way to really
# dig into the data, but can be overwhelming. The above plots (which
# show all data together) are probably your best first line of
# defense.

plotms(vis="sis14_twhya_calibrated.ms",
       xaxis="time",
       yaxis="phase",
       ydatacolumn="data",
       field="3",
       antenna="DV22&*",
       averagedata=T,
       avgchannel="1e6",
       iteraxis="antenna",
       coloraxis="corr",
       avgscan=True)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Flag your data
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# We decided to flag DV19 and DV01 for all scans, DV20 for scans
# 26-34, and channels 124-130 on Ceres (Field 2). We do this using the
# flagdata command in its "manual" mode.

# First flag the two antennas entirely.
flagdata("sis14_twhya_calibrated.ms",
         antenna="DV01,DV19")

# Now specify a scan range for DV20.
flagdata("sis14_twhya_calibrated.ms",
         antenna="DV20",
         scan="27~34")

# Finally, pick a field and a channel/spw range for Ceres.
flagdata("sis14_twhya_calibrated.ms",
         field="2",
         spw="0:124~130")

# We could split out the flagged data here, but we would rather take
# the knowledge of these flags back to the beginning of the
# calibration process. That is the next lesson.

# For now, go repeat the commands above to see the effect of your data
# flagging and convince yourself that these commands will remove most
# of the problems that you see in the data.


