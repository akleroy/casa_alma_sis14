# We have a line data cube and a continuum image. We'd now like to
# understand some of the properties of the images that we have
# produced. 

# Copy the data from the working directory
os.system("rm -rf sis14_twhya_cont.image")
os.system("cp -r ../working_data/sis14_twhya_cont.image .")

os.system("rm -rf sis14_twhya_n2hp.image")
os.system("cp -r ../working_data/sis14_twhya_n2hp.image .")

# Similar to listobs, you can orient yourself with these images using
# the image header command.

imhead("sis14_twhya_cont.image")
imhead("sis14_twhya_n2hp.image")

# ------------------------------
# STATISTICS
# ------------------------------

# Often some of the first numbers that you want to calculate are basic
# statistics and fluxes. You can do these pretty easily in the viewer,
# dragging out a box and then double clicking. You can also do this
# from the prompt.

imstat("sis14_twhya_n2hp.image",
       chans="0~4")

# The task returns a python dictionary (or just prints it to the
# shell). It's useful to see that the RMS is about 20 mJy/beam in the
# line cube.

# You can also use this for basic source characteristics. For example,
# calculate the statistics for a box encompasing the disk - the
# integrated flux is about 1.5 Jy...

imstat("sis14_twhya_cont.image",
       box="100,100,150,150")

# Alternatively, a box off the disk will give noise statistics.

imstat("sis14_twhya_cont.image",
       box="25,150,225,200")

# ------------------------------
# MOMENTS
# ------------------------------

# For the spectral line cube, it's very useful to collapse the cube in
# various ways to analyze the emission. The immoments task lets you do
# this. 

# ... make a moment 0 image clipped at ~1 sigma
os.system("rm -rf sis14_twhya_n2hp.mom0")
immoments("sis14_twhya_n2hp.image",
          outfile="sis14_twhya_n2hp.mom0",
          includepix=[20e-3,100],
          chans="4~12",
          moments=0)

# ... make a moment 1 image clipped at ~2 sigma
os.system("rm -rf sis14_twhya_n2hp.mom1")
immoments("sis14_twhya_n2hp.image",
          outfile="sis14_twhya_n2hp.mom1",
          includepix=[40e-3,100],
          chans="4~12",
          moments=1)

# At this point we have a few really neat things to see: first the
# line shows a hole in the middle. Overlay it on the dust (continuum)
# disk using the viewer and see that they align but with the N2H+
# existing only ouside a certain radius - in this case the snow line.

# Also have a look at the velocity field to see the rotation of the
# disk.


# Though it is only scriptable to a limited degree, imview does allow
# some basic command line plotting. This will overlay the line moment
# 0 on the continuum.

imview(raster={'file': 'sis14_twhya_cont.image',
               'range': [-0.01,0.5]},
       contour={'file': 'sis14_twhya_n2hp.mom0',
                'levels': [0.5,0.6,0.7,0.8] })

# ---------------------------------
# EXPORT FITS IMAGES
# ---------------------------------

# CASA is great (of course) but you will ultimately want to export
# your data to a common format to analyze in other programs, share
# with other astronomers, or archive. It's easy to export images from
# CASA's image format to .FITS images via the exportfits command.

exportfits(imagename="sis14_twhya_cont.image",
           fitsimage="twhya_cont.fits",
           overwrite=True)

# For the cube we want to specify additionally that the frequency axis
# will be written out as velocity.

exportfits(imagename="sis14_twhya_n2hp.image",
           fitsimage="twhya_n2hp.fits",
           velocity=True,
           overwrite=True)
