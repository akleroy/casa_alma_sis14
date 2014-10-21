# This script calibrates the amplitude and phase time dependence of
# the data. It also sets the flux scale of the data, based on a
# somewhat resolved planet. We start with the bandpass calibrated
# data.

# First, copy the data from the working directory
os.system("rm -rf sis14_twhya_bpcal.ms")
os.system("cp -r ../../working_data/sis14_twhya_bpcal.ms .")

# Orient yourself with a listobs
listobs("sis14_twhya_bpcal.ms")

# -=-=-=-=-=-=-=-= SET A MODEL FOR THE PLANET -=-=-=-=-=-=-=-= 

# First things first - we need to make sure that we have valid models
# in place for our data. We will work out the fluxes of the quasars
# later, for now it's good enough that we expect them to be point
# sources. However, the flux calibrator Ceres is somewhat resolved and
# we don't know the flux a priori. We need to read in a model from the
# solar system models that ship with CASA. We will use the task
# "setjy" and the library "Butler-JPL-Horizons 2012". With this call,
# we fill in the model column for Ceres.

setjy(vis="sis14_twhya_bpcal.ms",
      field="2",
      standard="Butler-JPL-Horizons 2012",
      usescratch=True)

# -=-=-=-=-=-=-=-= PHASE CALIBRATION -=-=-=-=-=-=-=-= 

# First, we calibrate the phase for each antenna for each scan. This
# is the right cadence to transfer to the science target, which is
# visited only on a ~ every-other-scan timescale.

os.system("rm -rf phase_scan.cal")
gaincal(vis="sis14_twhya_bpcal.ms",
        caltable="phase_scan.cal",
        field="0,2,3",
        solint="inf",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Plot the resulting phase calibration.

plotcal(caltable="phase_scan.cal", 
        xaxis="time",
        yaxis="phase",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,-180,180],
        markersize=10,
        fontsize=10.0,
        figfile="sis14_phase_scan.png")

# -=-=-=-=-=-=-=-= FLUX CALIBRATION -=-=-=-=-=-=-=-= 

# Flux calibration requires estimating the flux of the secondary
# calibrator. We will get there by bootstrapping from the flux of the
# primary calibrator (in this case the planet Ceres), which is known
# from a well understood model.

# Before we begin, we want to remove any short timescale phase
# variation from the sources involved in the flux calibration. Do so
# using gaincal.

os.system("rm -rf phase_int.cal")
gaincal(vis="sis14_twhya_bpcal.ms",
        caltable="phase_int.cal",
        field="0,2,3",
        solint="int",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Now plot the short timescale phase calibration to make sure it looks
# okay.

plotcal(caltable="phase_int.cal", 
        xaxis="time",
        yaxis="phase",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,-180,180],
        markersize=5,
        fontsize=10.0,
        figfile="sis14_phase_int.png")

# Our primary calibrator is a solar system body (Ceres). These can
# often be resolved, which can complicate any attempt to use them as
# calibrators. Best practice using these targets for flux calibration
# is to identify a subset of antennas or (more easily) a uv range over
# which the planetary disk shows a strong response. Look at the uv
# range of the model using plotms and try to identify such a range.

plotms(vis="sis14_twhya_bpcal.ms", 
       xaxis="uvdist", 
       yaxis="amp",
       ydatacolumn="model",
       field="2",
       averagedata=T, 
       avgchannel="1e3", 
       avgtime="1e3")

# It looks like 0~150m is probably a good u-v range to be able to
# calibrate using Ceres. Now let's run an amplitude solution, first
# applying the short-timescale phase solution *only for this u-v
# range.*

os.system("rm -rf apcal_shortuv.cal")
gaincal(vis="sis14_twhya_bpcal.ms",
        caltable="apcal_shortuv.cal",
        field="0,2,3",
        solint="inf",
        calmode="a",
        uvrange="0~150",
        gaintype="G",
        refant="DV22",
        gaintable="phase_int.cal")

# Plot this calibration, shwowing amplitude vs. time for each antenna.

plotcal(caltable="apcal_shortuv.cal", 
        xaxis="time",
        yaxis="amp",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,0,0])

# The gaincal solved for the amplitude scaling to make the data match
# the current model. For Ceres, we have taken care to set the correct
# model using setjy. For the other two calibrators, however, we don't
# a priori know the flux. Those have been calibrated using the default
# model, which is a point source of amplitude 1 Jy at the middle of
# the field. We now use fluxscale to bootstrap from the (correct) flux
# of Ceres through the amplitude calbiration table to estimates of the
# true flux of the other two calibrators. This will output both a new
# table and the flux estimates themselves.

os.system("rm -rf flux_shortuv.cal")
fluxscale(vis="sis14_twhya_bpcal.ms",
          caltable="apcal_shortuv.cal",
          fluxtable="flux_shortuv.cal",
          reference="2")

# Plot this rescaled flux table, which now should contain the correct
# flux calibrations. It will not be our final amplitude table, though,
# because we only solved over short u-v distance baselines.

plotcal(caltable="flux_shortuv.cal", 
        xaxis="time",
        yaxis="amp",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,0,0])

# -=-=-=-=-=-=-=-= AMPLITUDE CALIBRATION -=-=-=-=-=-=-=-= 
    
# From fluxscale, we see that we the two quasars have fluxes of ~0.65
# and ~8.4 Jy. Using the task setjy, we will adjust the model of these
# sources to reflect these flux estimates.

setjy(vis="sis14_twhya_bpcal.ms",
      field="3",
      fluxdensity = [0.65,0,0,0],
      usescratch=True)

setjy(vis="sis14_twhya_bpcal.ms",
      field="0",
      fluxdensity = [8.43,0,0,0],
      usescratch=True)

# Now we have the model correct for the two quasars, which - as point
# sources - are useful calibrators for all u-v ranges. We can run
# another amplitude solution without restricting the u-v range (though
# note that this will push things a bit on Ceres).

os.system("rm -rf flux.cal")
gaincal(vis="sis14_twhya_bpcal.ms",
        caltable="flux.cal",
        field="0,2,3",
        solint="inf",
        calmode="a",
        gaintype="G",
        refant="DV22",
        gaintable="phase_int.cal")

# This is our final flux calibration table. Inspect the amplitude
# corrections for each antenna.

plotcal(caltable="flux.cal", 
        xaxis="time",
        yaxis="amp",
        subplot=331,
        iteration="antenna",
        plotrange=[0,0,0,0])

# -=-=-=-=-=-=-=-= APPLY CALIBRATION -=-=-=-=-=-=-=-= 

# Apply our flux calibration and the (scan based) phase solution to
# all fields (including the science target).

# Note that we use the non-standard "calonly" command, which tells
# applycal not to flag data for which the calibration has failed.

applycal(vis="sis14_twhya_bpcal.ms",
         field="",
         gaintable=["phase_scan.cal",
                    "flux.cal"],
         interp="linear",
         applycal="calonly")

# -=-=-=-=-=-=-=-= INSPECT THE RESULTS  -=-=-=-=-=-=-=-= 

# Look at amplitude vs. time first in calibrated data and then in the
# model. We will go into much more detail on inspection and flagging
# in the next lesson.

plotms(vis="sis14_twhya_bpcal.ms", 
       xaxis="time", 
       yaxis="amp",
       ydatacolumn="corrected",
       field="0,2,3",
       averagedata=T, 
       avgchannel="1e3", 
       avgtime="1e3",
       coloraxis="field")

plotms(vis="sis14_twhya_bpcal.ms", 
       xaxis="time", 
       yaxis="amp",
       ydatacolumn="model",
       field="0,2,3",
       averagedata=T, 
       avgchannel="1e3", 
       avgtime="1e3",
       coloraxis="field")


# -=-=-=-=-=-=-=-= SPLIT OUT CALIBRATED DATA -=-=-=-=-=-=-=-= 

# Split out the calibrated data for future use. This is what you 

os.system("rm -rf sis14_twhya_calibrated.ms")
split(vis="sis14_twhya_bpcal.ms",
      outputvis="sis14_twhya_calibrated.ms",
      datacolumn="corrected",
      keepflags=False)
