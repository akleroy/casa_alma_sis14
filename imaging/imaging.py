# This script steps you through the basics of imaging your data. As a
# first step, we will image the calibrated data for our secondary
# quasar, which is just expected to be a point sources. 

# We will explore some of the options available to you in imaging and,
# as a demonstration, have a look at the effects of flagging and
# calibrating on imaging. We'll also see some of the tricks used to
# manage your data in CASA during imaging. Finally, we'll make our
# first image of the science source, imaging the dust continuum from
# the disk around TW Hydra.

# ---------------------
# SETUP AND ORIENTATION
# ---------------------

# Copy the calibrated and flagged data from the working
# directory. Remember that this is our best version of the data.

os.system("rm -rf sis14_twhya_calibrated_flagged.ms")
os.system("cp -r ../../working_data/sis14_twhya_calibrated_flagged.ms .")

# Orient yourself:
listobs('sis14_twhya_calibrated_flagged.ms')

# Plot the u-v coverage
plotms(vis='sis14_twhya_calibrated_flagged.ms',
       xaxis='u',
       yaxis='v',
       avgchannel='10000',
       avgspw=False,
       avgtime='1e9',
       avgscan=False,
       coloraxis="field")

# ---------------------
# FIRST CLEAN
# ---------------------

# Our secondary calibrator is field 3. Let's image field 2 into an
# image file called "secondary."

# First remove old versions of the image (the .* is needed because
# imaging produces several files with the same root name)
os.system('rm -rf secondary.*')

# Now use clean to image. We call the image secondary, target field 3,
# and use multifrequency synthesis (mode mfs) to make a single
# continuum image. We don't worry about frequency behavior and so set
# nterms=1. We set the cell size to 0.1 arcseconds (~4-5 pixels across
# a beam) and the image size to 128x128 (though factors of 2 are not
# magic for CASA). CLEAN will start in interactive mode.

clean(vis='sis14_twhya_calibrated_flagged.ms',
      imagename='secondary',
      field='3',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[128,128],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True)

# In the CLEAN viewer, make sure that your buttons are set to add a
# new reckangle. Draw a box around the source (just the central
# dot). Double click inside the box and watch it turn white.

# When you are satisfied that you have captured the emission and not
# much else, hit the green circle button. This will run a major cycle
# of cleaning and then return.

# CLEAN will come back and show you the emission left after the major
# cycle. Look at those gorgeous residuals! When you are satisfied (or
# when CLEAN thinks that the cleaning has met the threshold, 0 mJy by
# default - meaning that it stops at the first negative) hit the red X
# and CLEAN will terminate.

# Have a quick look at the files that it has created
os.system("ls")

# the .image file is the image, the .mask shows where you cleaned, the
# .model is the model used by clean (in Jy/pixel), the .flux shows the
# primary beam response, the .residual shows what was left after you
# cleaned (the "dirty" part of the final image), and the .psf file
# shows the synthesized beam. So much good stuff.

# Look at any of these using the CASA viewer. This can be started with
# "viewer()", externally via casaviewer or targeting a specific image
# via "imview"
imview("secondary.image")

# Look at the other images now (load them interactively using the
# viewer)

# ---------------------
# EXPERIMENT WITH CLEAN
# ---------------------

# CLEAN exposes a lot of options. Now is a good time to get a feel for
# what these can do. One that is commonly tweaked by the user is the
# weighting scheme used to grid the u-v data into a fourier-plane
# image. This weighting was "natural" in the first example. Try
# changing it to "briggs" here and try a few different values of the
# robust parameter. Pay attention to how the beam size changes (as
# well as the noise in the final image, measured by drawing a box and
# double clicking).

# Remove old versions
os.system('rm -rf secondary_robust.*')

# Clean
clean(vis='sis14_twhya_calibrated_flagged.ms',
      imagename='secondary_robust',
      field='3',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[128,128],
      cell=['0.1arcsec'],
      weighting='briggs',
      robust=-1.0,
      threshold='0mJy',
      interactive=True)

# Look at the results
imview("secondary_robust.image")

# Now is a good time to experiment a bit with CLEAN - try imaging the
# other calibrator fields (0 and 2) and making the image size larger
# and smaller.

# Here are a few possible things you might try...

# Look at the marginally resolved Ceres
os.system('rm -rf primary_robust.*')
clean(vis='sis14_twhya_calibrated_flagged.ms',
      imagename='primary_robust',
      field='2',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[128,128],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True)
imview("primary_robust.image")

# Notice that if you look carefully you can see that Ceres is somewhat
# resolved, leading to the uv distance issues we had to deal with in
# our flux calibration.

# Try a really big pixel size and watch things break
os.system('rm -rf secondary_bigpix.*')
clean(vis='sis14_twhya_calibrated_flagged.ms',
      imagename='secondary_bigpix',
      field='3',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[32,32],
      cell=['0.5arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True)
imview("secondary_bigpix.image")

# To see the issues clearly here, compare the beam in this image to
# the one in the first image we made (with 5x smaller pixels).

# -------------------------------------------
# SEE THE EFFECTS OF CALIBRATION AND FLAGGING
# -------------------------------------------

# (This is an aside intended to be instructive, but you can skip it if
# you are in a hurry.)

# We went to a lot of trouble to flag and calibrate the data... what
# effect did this actually have? As an instructive aside, let's image
# the secondary calibrator with and without calibration and with and
# without flagging just to get an idea.

# Copy the uncalibrated data.
os.system("rm -rf sis14_twhya_uncalibrated.ms")
os.system("cp -r ../../working_data/sis14_twhya_uncalibrated.ms .")

# Clean
os.system('rm -rf secondary_uncalibrated.*')
clean(vis='sis14_twhya_uncalibrated.ms',
      imagename='secondary_uncalibrated',
      field='3',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[128,128],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True)

# If you can find a source to clean, more power to you! It's a good
# thing that we calibrated... In the raw (but still Tsys and WVR
# corrected) data you can see echos of the calibrator throughout the
# field, but the calibration makes the image coherent.

imview("secondary_uncalibrated.image")

# Copy the unflagged data
os.system("rm -rf sis14_twhya_calibrated.ms")
os.system("cp -r ../../working_data/sis14_twhya_calibrated.ms .")

os.system('rm -rf secondary_unflagged.*')
clean(vis='sis14_twhya_calibrated.ms',
      imagename='secondary_unflagged',
      field='3',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[128,128],
      cell=['0.1arcsec'],
      weighting='natural',
      threshold='0mJy',
      interactive=True)

imview("secondary_unflagged.image")

# In contrast to the uncalibrated data, the unflagged data are
# coherent, but they have clear artifacts in the residuals. Flagging
# is clearly improving the quality of the data, but in overall good
# quality data like we have here, it's already possible to see the
# source.

# ------------------------
# IMAGE THE SCIENCE TARGET
# ------------------------

# Of course, the whole point of calibration is to calibrate the
# science data (here field 5, check the listobs). As the final step in
# the imaging tutorial, let's now do that. We will make a first
# continuum image of TW Hydra.

# First, we will split out the science data into its own data set,
# while not strictly necessary this is a common step that makes
# managing the data easier. At the same time we will smooth the data
# in frequency using a call of width=10 to smooth. This reduces the
# data volume without losing much information (because we are doing
# continuum imaging). This is a good tool to keep in mind for very
# large volume data sets (here it's less of an issue because we have
# designed the data set to be manageable).

os.system('rm -rf twhya_smoothed.ms')
split(vis='sis14_twhya_calibrated_flagged.ms',
      field='5',
      width='10',
      outputvis='twhya_smoothed.ms',
      datacolumn='data')
listobs('twhya_smoothed.ms')

# Now make a continuum image of the split out data. Notice that now TW
# Hydra is field 0.

os.system('rm -rf twhya_cont.*')
clean(vis='twhya_smoothed.ms',
      imagename='twhya_cont',
      field='0',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[250,250],
      cell=['0.08arcsec'],
      weighting='briggs',
      robust=0.5,
      threshold='0mJy',
      interactive=True)

# Clean until the emission from the TW Hydra disk is less than or
# comparable to the residuals around it.

# Have a look at the image - TW Hydra is very bright and very extended
# relative to the beam. The residuals aren't perfect, but we will
# improve them in subsequent lessons.
imview("twhya_cont.image")

# ------------------------
# NONINTERACTIVE CLEAN
# ------------------------

# So far we have mostly followed an interactive process with
# CLEAN. CLEAN can also be set up to run without interactice
# guidance. The three main parameters to specify are the threshold at
# which to stop (when the maximum residual is lower than this
# threshold, CLEAN stops), the mask (the region in which CLEAN is
# willing to identify signal), and the maximum number of iterations
# (though this is not a recommended way to steer clean).

# Look at the image you just made and figure out a box that holds TW
# Hydra. Something like 100,100 to 150,150 seems good for the above
# image size. We'll set that box to be a mask using the "mask"
# parameter.

# We also need to specify a stopping threshold for CLEAN. Again, look
# at the previous image and drag a box well away from the source to
# estimate the noise. We see something like ~7 mJy/beam. Set the
# threshold to be about twice this, ~15 mJy/beam.

# Finally set niter=5000, which is a lot of iterations - we expect
# CLEAN to terminate before reaching this. For our purposes this is
# just a big number.

os.system('rm -rf twhya_cont_auto.*')
clean(vis='twhya_smoothed.ms',
      imagename='twhya_cont_auto',
      field='0',
      spw='',
      mode='mfs',
      nterms=1,
      imsize=[250,250],
      cell=['0.08arcsec'],
      mask='box [ [ 100pix , 100pix] , [150pix, 150pix ] ]',
      weighting='briggs',
      robust=0.5,
      threshold='15mJy',
      niter=5000,
      interactive=False)

imview('twhya_cont_auto.image')

# Looks ma, no hands!
