# This script steps you through continuum imaging and self calibration
# of the science data for our science target, TW Hydra. You already
# made a first continuum image in the earlier imaging lesson. We start
# by repeating that step and then we iteratively self calibrate the
# data, focusing on short-timescale phase corrections.

# Copy the calibrated and flagged data from the working
# directory. Remember that this is our best version of the data.

os.system("rm -rf sis14_twhya_calibrated_flagged.ms")
os.system("cp -r ../working_data/sis14_twhya_calibrated_flagged.ms .")

# Run a quick listobs to get situated
listobs("sis14_twhya_calibrated_flagged.ms")

# First, use clean to make a continuum image of TW Hydra (field
# 5). This is inteactive, but the automated approach that we used in
# the last lesson would also work. Clean now until the residuals near
# TW HYdra are comparable to those in the rest of the image.

os.system('rm -rf first_image.*')
clean(vis='sis14_twhya_calibrated_flagged.ms',
      imagename='first_image',
      field='5',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[250,250],
      cell=['0.08arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True)

# In addition to creating an image, CLEAN saves the cleaned model with
# the measurement set. This means that based on the previous clean, we
# now have a model for the science target. In the previous calibration
# we only had models for the calibrators. Of course this model is only
# as good as the first clean, but it's a good starting point.

# With a model in place, we are now in a position to calibrate the
# science target directly. We use gaincal just like we would for any
# other calibration. We focus on phase corrections - generally good
# practice for self calibration - because amplitude self calibration
# has a larger potential to change the source characteristics.

# Figuring out the right averaging is often the key to good
# self-calibration. Ideally, you would like to work with the shortest
# solution interval possible (and to keep separate spws and
# polarizations if possible). However, for faint sources it's often
# necessary to average data in various ways to achieve good
# solutions. The choice of 30 seconds below is a good option for TW
# Hydra.

os.system("rm -rf phase.cal")
gaincal(vis="sis14_twhya_calibrated_flagged.ms",
        caltable="phase.cal",
        field="5",
        solint="30s",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Try playing around with different solution intervals or options.

# Plot the resulting solutions. We are finding nontrivial, though not
# enormous, offsets (a few 10s of degrees) with the two correlations
# tracking one another pretty well.

plotcal(caltable="phase.cal", 
        xaxis="time",
        yaxis="phase",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,-30,30],
        markersize=5,
        fontsize=10.0,
        figfile="sis14_selfcal_phase_scan.png")

# We are happy with this solution. Apply it to the data using
# applycal. We only care about field 5 (the science target) at this
# point.

applycal(vis="sis14_twhya_calibrated_flagged.ms",
         field="5",
         gaintable=["phase.cal"],
         interp="linear")

# At this point the self-calibrated data live in the corrected
# column. Because we will want to try more rounds of self calibration,
# it's very useful (though not strictly necessary) at this point to
# split out the corrected data into a new data set.

os.system("rm -rf sis14_twhya_selfcal.ms")
split(vis="sis14_twhya_calibrated_flagged.ms",
      outputvis="sis14_twhya_selfcal.ms",
      datacolumn="corrected"
      )

# Now clean the self-calibrated data. Again, clean until the residuals
# on TW Hydra resemble those in the surrounding image. 

os.system('rm -rf second_image.*')
clean(vis='sis14_twhya_selfcal.ms',
      imagename='second_image',
      field='5',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[250,250],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True,
      niter=5000)

# The residuals do look better this time around. Run the viewer and
# compare the first and second images. You should see a notable
# improvement in the noise and some improvement in the signal, so that
# the overall signal-to-noise (dynamic range).

# This second clean also produces a model, hopefully a mildly 

os.system("rm -rf phase_2.cal")
gaincal(vis="sis14_twhya_selfcal.ms",
        caltable="phase_2.cal",
        field="5",
        solint="30s",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Plot calibration - at this point, we see much smaller phase scatter
# relative to the model, so we don't expect more self calibration to
# do much.

plotcal(caltable="phase_2.cal", 
        xaxis="time",
        yaxis="phase",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,-30,30],
        markersize=5,
        fontsize=10.0,
        figfile="sis14_selfcal_phase_scan_2.png")

# Apply again
applycal(vis="sis14_twhya_selfcal.ms",
         field="5",
         gaintable=["phase_2.cal"],
         interp="linear")

# Split again - here you can see the work flow for heavily iterative
# self-calibration. We progressively calibrate, split.

os.system("rm -rf sis14_twhya_selfcal_2.ms")
split(vis="sis14_twhya_selfcal.ms",
      outputvis="sis14_twhya_selfcal_2.ms",
      datacolumn="corrected"
      )

# Clean a third time.

os.system('rm -rf third_image.*')
clean(vis='sis14_twhya_selfcal_2.ms',
      imagename='third_image',
      field='5',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[250,250],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True,
      niter=5000)

# The improvement is really marginal at this point. Confident that we
# have done what we can on the phase, we can experiment with amplitude
# self calibration. This is potentially dangerous as it has much more
# potential to change the characteristics of the source than phase
# self-calibration. We mitigate this somewhat by setting solnorm=True,
# so that the solutions are normalized.

os.system("rm -rf amp.cal")
gaincal(vis="sis14_twhya_selfcal_2.ms",
        caltable="amp.cal",
        field="5",
        solint="30s",
        calmode="ap",
        refant="DV22",
        gaintype="G",
        solnorm=True)

# Plot the amplitude solutions.

plotcal(caltable="amp.cal", 
        xaxis="time",
        yaxis="amp",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,0,0],
        markersize=5,
        fontsize=10.0)

# We see a good deal of scatter and some offsets between
# correlations. It is at least worth looking at what the effects of
# applying this will be.

applycal(vis="sis14_twhya_selfcal_2.ms",
         field="5",
         gaintable=["amp.cal"],
         interp="linear")

# At this point the self-calibrated data live in the corrected
# column. Because we will want to try more rounds of self calibration,
# it's very useful (though not strictly necessary) at this point to
# split out the corrected data into a new data set.

os.system("rm -rf sis14_twhya_selfcal_3.ms")
split(vis="sis14_twhya_selfcal_2.ms",
      outputvis="sis14_twhya_selfcal_3.ms",
      datacolumn="corrected"
      )

# Clean a fourth time.

os.system('rm -rf fourth_image.*')
clean(vis='sis14_twhya_selfcal_3.ms',
      imagename='fourth_image',
      field='5',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[250,250],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True,
      niter=5000)

# As you push the clean down, the background now looks very random on
# the scale of the beam. This is good!

# Compare the third and fourth images. The noise has made a dramatic
# improvement, while the flux has not changed markedly (this is very
# good, it's what we worry about with amplitude self calibration).

# By assuming that the previous cleans represent good models we have
# managed to improve the signal-to-noise on the data by almost an
# order of magnitude. Not bad!

# This fourth image is our best continuum image. We can use the data
# set (selfcal_3) to for further work - in the next lesson we'll do uv
# continuum subtraction and line imaging.
