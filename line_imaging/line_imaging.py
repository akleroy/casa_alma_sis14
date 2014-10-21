# This lesson steps you through imaging of spectral lines. We start
# with the self-calibrated data from the previous lesson. We could
# just as easily begin with the non self-calibrated data, but we would
# not then benefit from the improvements that the self calibration
# provided.

# As an aside it is often, but by no means always, the case that it
# makes sense to self calibrate on the continuum for line science
# projects that target bright continuum sources; sometimes it does
# make sense to attempt self-calibration on the line (but this is a
# more advanced topic).

# First, copy the self-calibrated measurement set, which still
# contains both line and continuum data for all targets, to the
# current directory.

os.system("rm -rf sis14_twhya_selfcal.ms")
os.system("cp -r ../../working_data/sis14_twhya_selfcal.ms .")

# ------------------------
# UV CONTINUUM SUBTRACTION
# ------------------------

# Out first step to make a line image is to remove continuum emission
# from the data. Here continuum emission means broadband emission
# present across all spectral channels (though perhaps with some
# frequency dependent amplitude). The cleanest way to do this is to
# subtract the continuum from the u-v data visibility by visibility,
# fitting its amplitude from line-free spectral channels. We will do
# so using the CASA task uvcontsub.

# The main subtlety using the uv continuum subtraction is that we want
# to be sure to only fit the continuum using channels that contain
# mostly continuum (and not line) emission. To this end, the first
# thing that we will do is plot the integrated spectrum of the source
# using the PLOTMS command. We target the science source (field 5) and
# plot the amplitude as a function channel, averaging together all
# times (allowing averaging across scans via avgscan=True).

plotms(vis='sis14_twhya_selfcal.ms',
       xaxis='channel',
       yaxis='amp',
       field='5',
       avgspw=False,
       avgtime='1e9',
       avgscan=True,
       avgbaseline=True)

# Inside the PLOTMS tabs, you can toggle the axis to frequency and
# then back to channel - the N2H line is at 372.67249 GHz and there is
# a weak but still visible spectral line in the range of channels
# ~260-280. The rest of the spectrum seems viable for continuum. We
# could reasonably decide that channels 240-280 hold some line
# emission and should thus be avoided.

# Carry out a continuum subtraction, avoiding channels 240-280 (we set
# fitspw='0:240~280' and then set excludechans=True to tell CASA that
# these are the channels NOT to fit). Fit only a constant amplitude
# continuum by setting the fitorder to 0 and target only field '5',
# the science source.

os.system('rm -rf sis14_twhya_selfcal.ms.contsub')
uvcontsub(vis = 'sis14_twhya_selfcal.ms',
          field = '5',
          fitspw = '0:240~280',
          excludechans = True,
          fitorder = 0)

# The output is a continuum subtracted data set that has the
# additional extension ".contsub". We can now plot that using PLOTMS,
# similar to what we did before, and look at the spectrum, which
# should not contain only the spectral line. Note that because we only
# rang uvcontsub on field '5' above, it is now field '0' (the first
# and only field) in the new measurement set. Run a listobs on the
# continuum subtracted data to see this.

plotms(vis='sis14_twhya_selfcal.ms.contsub',
       xaxis='channel',
       yaxis='amp',
       field='0',
       avgspw=False,
       avgtime='1e9',
       avgscan=True,
       avgbaseline=True)

# It looks reasonably continuum-subtracted. We'll see better from the
# image. (Note that because the amplitude is positive definite, you
# don't expect the line free channels to go entirely to zero, just to
# average to a very small value that reflects the noise.)

# ------------------------
# IMAGE THE LINE
# ------------------------

# Line imaging is like continuum imaging with (as you would expect)
# the additional dimension of spectral information. In the call to
# clean, you now need to specify the frequency grid onto which the
# data will be placed. This can be done in units of channel
# (mode="channel"), velocity (mode="velocity"), or frequency
# (mode="frequency"). Any are a valid approach for these data. 

# Below, we use mode="velocity" and specify 0.5 km/s-wide planes in
# the output cube, imaging 15 such planes starting at 0 km/s LSRK. The
# velocity is defined relative to the N2H+ rest frequency that we
# pulled from splatalogue earlier.

# Define the N2H+ rest frequency as a variable here:
restfreq = '372.67249GHz'

# Now we use CLEAN to make the cube - we specify interactive mode, so
# that the viewer will come up. When it does, scroll through the
# channels in the cube using the animator. We see emission over a few
# channels near the center of the cube with the location of emission
# shifting by channel (which is neat, this is velocity structure from
# the rotating disk!). You can put a big box across all channels to
# circle the emission (see the button at the top that toggles whether
# your mask applies to all planes) or you can carefully circle the
# emision that looks real in each channel. Both are viable approaches,
# but for a high fidelity telescope like ALMA it's often (but not
# always) good enough to put one mask across all channels.

# Now call CLEAN targeting the continuum subtracted data, field '0'
# and spw '0' (the only optinos in this data set), in mode 'velocity'
# with 15 channels of 0.5 km/s starting at 0.0 km/s defined in the
# LSRK frame (a common frame for Galactic and extragalactic
# work). Otherwise, this call will resemble our previous calls.

os.system('rm -rf twhya_n2hp.*')
clean(vis = 'sis14_twhya_selfcal.ms.contsub',
  imagename = 'twhya_n2hp',
  field = '0',
  spw = '0',
  mode = 'velocity',
  nchan = 15,
  start = '0.0km/s',
  width = '0.5km/s',
  outframe = 'LSRK',
  restfreq = restfreq,
  interactive = T,
  imsize = [250, 250],
  cell = '0.08arcsec',
  phasecenter = 0,
  weighting = 'briggs',
  robust = 0.5)

# The output of the cleaning here is a cube - use the viewer to
# inspect the cube, plot spectra, estimate the noise, and overlay this
# result with the earlier continuum image.

imview("twhya_n2hp.image")

# At this point you should feel free to play with the velocity axis
# definitions, mess around with the viewer, and so on. Our next lesson
# will go through how to make some basic analysis plots for the cube.
