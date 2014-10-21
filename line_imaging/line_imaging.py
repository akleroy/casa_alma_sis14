# This lesson steps you through imaging of spectral lines. We start
# with the self-calibrated data from the previous lesson. We could
# just as easily begin with the non self-calibrated data, but would
# not then benefit from the improvements that the self calibration
# provided.

# Copy the working data

# Copy the data from the working directory
os.system("rm -rf sis14_twhya_selfcal.ms")
os.system("cp -r ../../working_data/sis14_twhya_selfcal.ms .")

# ------------------------
# UV CONTINUUM SUBTRACTION
# ------------------------

# Out first step to make a line image is to remove the continuum
# emission from the data. The cleanest way to do this is to subtract
# the continuum from the u-v data visibility by visibility. We will do
# so using the task uvcontsub.

# The main subtlety using the uv continuum subtraction is that we want
# to be sure to only fit the continuum using channels that are mostly
# continuum. To this end, the first thing that we will do is just plot
# the integrated spectrum of the source.

# Plot a spectrum
plotms(vis='sis14_twhya_selfcal.ms',
       xaxis='channel',
       yaxis='amp',
       field='5',
       avgspw=False,
       avgtime='1e9',
       avgscan=True,
       avgbaseline=True)

# Toggle to frequency - N2H is at 372.67249 GHz and there is a
# somewhat visible spectral line in the range of channels
# ~260-280. The rest of the spectrum seems viable for continuum.

# Do a rough continuum subtraction, avoiding channels 240-280.
os.system('rm -rf sis14_twhya_selfcal.ms.contsub')
uvcontsub(vis = 'sis14_twhya_selfcal.ms',
          field = '5',
          fitspw = '0:240~280',
          excludechans = True,
          fitorder = 0)

# Plot the continuum-subtracted spectrum
plotms(vis='sis14_twhya_selfcal.ms.contsub',
       xaxis='channel',
       yaxis='amp',
       field='0',
       avgspw=False,
       avgtime='1e9',
       avgscan=True,
       avgbaseline=True)

# It looks reasonably continuum-subtracted. We'll see better from the
# image.

# ------------------------
# IMAGE THE LINE
# ------------------------

# Line imaging is like continuum imaging with (as you would expect)
# the additional dimension of spectral information. In the call to
# clean, you now need to specify the frequency grid onto which the
# data will be placed. This can be done in units of channel, velocity
# or frequency. Any are a valid approach for these data. Below, we
# specify half kilometer a second channels, 15 of them starting at 0
# km/s LSRK. The velocity is defined relative to the N2H+ rest
# frequency that we pulled from splatalogue earlier.

# N2H+ rest frequency
restfreq = '372.67249GHz'

# Make the cube - we specify interactive mode, so that the viewer will
# come up. When it does, we see emission over a few channels near the
# center of the cube with the location of emission shifting by channel
# (which is neat!). You can put a big box across all channels to
# circle the emission or you can carefully circle the emision that
# looks real in each channel. Both a viable approaches.

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
  imagermode = 'mosaic',
  interactive = T,
  imsize = [250, 250],
  cell = '0.08arcsec',
  phasecenter = 0,
  weighting = 'briggs',
  robust = 0.5)

# The output of the cleaning here is a cube - use the viewer to
# inspect the cube, plot spectra, etc.

imview("twhya_n2hp.image")

# At this point you should feel free to play with the velocity axis
# definitions, mess around with the viewer, and so on. Our next lesson
# will go through how to make some basic analysis plots for the cube.
