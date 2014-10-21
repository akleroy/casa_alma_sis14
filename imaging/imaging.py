# This script steps you through the basics of imaging your data. As a
# first step, we will image the calibrated data for our secondary
# quasar, which is just expected to be a point source.

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

# Our secondary calibrator (also called the phase calibrator) is field
# 3. Let's image this field into an image file called "secondary."

# First remove old versions of the image (the .* is needed because
# imaging produces several files with the same root name)

os.system('rm -rf secondary.*')

# Now use CLEAN to image. We call the image "secondary", specify that
# we want to image the data for field "3", and use multifrequency
# synthesis (mode mfs) to make a single continuum
# image. Multifrequency synthesis combines data from all selected
# spectral channels into a single continuum image. Because the
# fractional bandwidth (delta nu/nu) is pretty small, we will not
# worry about the amplitude or structure of the source changing
# substantially with frequency behavior. Therefore, we set nterms=1,
# telling CLEAN that each deconvolved component has a single amplitude
# at all frequencies. We set the cell size to 0.1 arcseconds, which
# places ~4-5 pixels across a beam (you could figure this out a
# priori, but it is often easier to just experiment with a quick
# imaging call and note the beam calculated by CLEAN). We set the
# image size to 128x128 (but note that factors of 2 are not magic for
# CASA). This is enough to get most of the primary beam but we might
# want a wider field for a non point source. CLEAN will start in
# interactive mode, which allows you to manually control the
# threshold, major cycles, and masking..

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

# When you are satisfied that you have captured the real emission and
# not much else, hit the green circle button. This will run a major
# cycle of cleaning and then return. Remember that the secondary
# calibrator has been picked to give you just a point source at the
# middle of the field.

# CLEAN will come back and show you the emission left after the major
# cycle. Look at those gorgeous residuals! When you are satisfied (or
# when CLEAN thinks that the CLEANing has met the threshold, 0 mJy by
# default - meaning that it stops at the first negative) hit the red X
# and CLEAN will terminate.

# Have a quick look at the files that CLEAN has created:
os.system("ls")

# the .image file is the image, the .mask shows where you CLEANed, the
# .model is the model used by CLEAN (in Jy/pixel), the .flux shows the
# primary beam response, the .residual shows what was left after you
# CLEANed (the "dirty" part of the final image), and the .psf file
# shows the synthesized beam. So much good stuff.

# Look at any of these using the CASA viewer. This can be started with
# "viewer()", externally via casaviewer or targeting a specific image
# via "imview"
imview("secondary.image")

# Look at the other images now (load them interactively using the
# viewer).

# ---------------------
# EXPERIMENT WITH CLEAN
# ---------------------

# CLEAN exposes a lot of options. Now is a good time to get a feel for
# what these can do. One option that is very commonly tweaked by the
# user is the weighting scheme used to grid the u-v data into a
# fourier-plane image. This weighting was "natural" in the first
# example (by default). Try changing it to "briggs" here and try a few
# different values of the robust parameter. Pay attention to how the
# beam size changes (as well as the noise in the final image, measured
# by drawing a box and double clicking in the viewer after the fact).

# Remove old versions of the image in case you have run this before
os.system('rm -rf secondary_robust.*')

# Call CLEAN with briggs weighting and robust = -1
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

# Look at the marginally resolved calibrator Ceres (field 2)
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
# resolved, leading to changing amplitude as a function of uv distance
# that we had to deal with in our flux calibration (and can be seen
# still from a basic plotms).

# Try a really big pixel size and watch things break. It is
# recommended to have the pixel size small compared to the synthesized
# beam for CLEANing purposes (CLEAN quantizes the deconvolution in
# units of pixels). When the pixel size is big compared to the
# synthesized beam the imaging in general will start to degrade, even
# independent of CLEANing.

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

# NOTE: This is an aside intended to demonstrates the effect of
# calibration, you can skip it if you are in a hurry or are focused on
# learning only imaging.

# We went to a lot of trouble to flag and calibrate the data... what
# effect did this actually have? Let's image the secondary calibrator
# with and without calibration and with and without flagging just to
# get an idea of how our processing changed the final image.

# Copy the uncalibrated data from the working directory.
os.system("rm -rf sis14_twhya_uncalibrated.ms")
os.system("cp -r ../../working_data/sis14_twhya_uncalibrated.ms .")

# CLEAN the uncalibrated data, again focus on the secondary calibrator
# (field 3) and use the same calls as before.
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

# If you can find a source to CLEAN then more power to you, but this
# is a mess. It's a good thing that we calibrated... In the raw (but
# still Tsys and WVR corrected) data you can see echos of the
# calibrator throughout the field, but the calibration is required to
# make the image coherent.

# Inspect the imaged uncalibrated data using the CASA viewer:
imview("secondary_uncalibrated.image")

# Now let's see the effect of flagging. Copy the unflagged data from
# the working directory to our local directory:
os.system("rm -rf sis14_twhya_calibrated.ms")
os.system("cp -r ../../working_data/sis14_twhya_calibrated.ms .")

# Not image the unflagged data for the secondary calibrator using the
# same parameters as before.

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
# is definitely improving the quality of the data, but in overall good
# quality data like we have here, it's already possible to see the
# source before the additional flagging that we did.

# ------------------------
# IMAGE THE SCIENCE TARGET
# ------------------------

# Of course, the whole point of calibration is to calibrate the
# *science* data (here field 5, which we know from our listobs
# above). As the final step in the basic imaging tutorial, let's now
# do that. We will make a first continuum image of TW Hydra.

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
# Hydra is field 0 in the new data set because we split out only that
# field. Again we will use the multifrequency synthesis mode ("mfs")
# and we will use both a somewhat smaller pixel size and a somewhat
# bigger image size than above (because TW Hydra is extended and and
# the beam will be somewhat smaller due to our use of "briggs"
# weighting). Again, specify interactive mode and leave the threshold
# unset for the time being.

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

# Draw a box around the visible emission using the toolbar and then
# CLEAN until the emission from the TW Hydra disk is less than or
# comparable to the residuals around it. You will decide when CLEAN
# should stop, at which point you hit the red X. Therefore you don't
# need to set the threshold in this case. If you did want to place an
# automated cutoff point, you could specify a threshold that is a
# small multiple of the rms noise either in the call to CLEAN above or
# by typing it in to the viewer window. We'll see more on this below.

# Have a look at the image - TW Hydra is very bright and very extended
# relative to the beam. The residuals aren't perfect, but we will
# improve them in subsequent lessons.
imview("twhya_cont.image")

# ------------------------
# NONINTERACTIVE CLEAN
# ------------------------

# So far we have mostly followed an interactive process with
# CLEAN. CLEAN can also be set up to run without interactive
# guidance. The three main parameters to specify are the threshold at
# which to stop (when the maximum residual is lower than this
# threshold, CLEAN stops), the mask (the region in which CLEAN is
# willing to identify signal), and the maximum number of iterations
# (though this is not required and it is generally recommended that
# this be used as more of a failsafe - set it to a number so high that
# if CLEAN gets there something has gone wrong).

# Look at the image you just made and figure out a box that holds TW
# Hydra. Something like 100,100 to 150,150 seems good for the above
# image size. We'll set that box to be a mask using the "mask"
# parameter in the call to clean. You could also set it by supplying a
# file (for example that created from your earlier interactive version
# of clean).

# We also need to specify a stopping threshold for CLEAN. Again, look
# at the previous image and drag a box well away from the source to
# estimate the noise. We see something like ~7 mJy/beam. Set the
# threshold to be about twice this, ~15 mJy/beam. A clean threshold
# several times the rms noise is usually recommended in order to avoid
# adding false sources to the deconvolved image (that is, you do not
# want clean to treat a random noise spike as a source and deconvolve
# it from the image; particularly in the case of later
# self-calibration this can cause real problems).

# Finally set niter=5000, which is a lot of iterations - we expect
# CLEAN to terminate before reaching this. For our purposes this is
# just a big number that's designed to keep CLEAN from running
# forever.

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

# This noninteractive mode can save you a lot of time and has the
# advantage of being very reproducible. Note that you also have a
# "hybrid" mode available by starting the CLEAN process with
# interactive=True but then hitting the arrow button in the top right
# corner. This tells CLEAN to proceed until it hits the maximum number
# of iterations or the threshold. This combination mode is nice
# because you can manually draw the mask used to clean. Note that you
# can also manually set both the threshold and the maximum number of
# iterations (which is the product of the number of major cycles and
# the iterations per cycle) in the viewer.

# Note, however, that best practice for an image with uncertain
# calibration and especially one with a bright source, is to clean
# interactively at least the first time. In the case where an image
# may be "dynamic range limited" (i.e., the quality is set by the
# accuracy of calibration and deconvolution) it can be hard to predict
# the correct threshold.

# ------------------------
# PRIMARY BEAM CORRRECTION
# ------------------------

# An important subtlety of CLEAN is that by default the image produced
# by CLEAN is not corrected for the primary beam (the field of view)
# of the individual dishes in the array. The primary beam response is
# typically a Gaussian with value 1 at the center of the field. To
# form an astronomically correct image of the sky, the output of CLEAN
# needs to be divided by this primary beam (or, in the case of
# mosaics, the combination of primary beam patterns used to make the
# mosaic). Fortunately, CASA stores the primary beam information
# needed to make this correction in an image file with a ".flux"
# extension.

# The CASA task impbcor can be used to combine the .flux image with
# the output image from CLEAN to produce a primary-beam corrected
# image.

# First remove the old primary beam corrected image if it exists
os.system('rm -rf twhya_cont.pbcor.image')

# Now correct the image
impbcor(imagename='twhya_cont.image',
        pbimage='twhya_cont.flux',
        outfile='twhya_cont.pbcor.image')

# Inspect the output image
imview('twhya_cont.pbcor.image')

# It's often very convenient to work in images before primary beam
# correction because the noise is the same across the field (e.g.,
# this is a clean data set to search for signal) but it's very
# important to remember to apply this correction before calculating
# fluxes or intensities for science.
