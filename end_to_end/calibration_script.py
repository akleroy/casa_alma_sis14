# Run end-to-end calibration on a measurement set with name held by
# the variable vis.

# --------------------
# RESET
# --------------------

# Start by removing previous calibrations
clearcal(vis+".ms")

# --------------------
# BANDPASS CALIBRATION
# --------------------

# A short-timescale phase solution
os.system("rm -rf phase_int_bp.cal")
gaincal(vis=vis+".ms",
        caltable="phase_int_bp.cal",
        field="0",
        solint="int",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Calibrate the bandpass
os.system("rm -rf bandpass_10chan.cal")
bandpass(vis=vis+".ms",
         caltable="bandpass_10chan.cal",
         field="0",
         refant="DV22",
         solint="inf,10chan",
         combine="scan",
         gaintable=["phase_int_bp.cal"])

# Apply
applycal(vis=vis+".ms",
         gaintable=["bandpass_10chan.cal"],
         interp=["nearest"],
         gainfield=["0"])

os.system("rm -rf "+vis+"_bpcal.ms")
split(vis=vis+".ms",
      datacolumn="corrected",
      outputvis=vis+"_bpcal.ms",
      keepflags=False)

# ---------------------
# SET CALIBRATOR FLUXES
# ---------------------

# Use the fluxes that we know from earlier

# Look up the model for ceres
setjy(vis=vis+"_bpcal.ms",
      field="2",
      standard="Butler-JPL-Horizons 2012",
      usescratch=True)

# Set the model for the bandpass calibrator
setjy(vis=vis+"_bpcal.ms",
      field="0",
      fluxdensity = [8.43,0,0,0],      
      usescratch=True)

# Set the model for the secondary calibrator
setjy(vis=vis+"_bpcal.ms",
      field="3",
      fluxdensity = [0.65,0,0,0],      
      usescratch=True)

# -------------------
# PHASE AND AMPLITUDE
# -------------------

# Derive a short-timescale phase solution
os.system("rm -rf phase_int.cal")
gaincal(vis=vis+"_bpcal.ms",
        caltable="phase_int.cal",
        field="0,2,3",
        solint="int",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Calibrate the phase
os.system("rm -rf phase_scan.cal")
gaincal(vis=vis+"_bpcal.ms",
        caltable="phase_scan.cal",
        field="0,2,3",
        solint="inf",
        calmode="p",
        refant="DV22",
        gaintype="G")

# Calibrate the amplitude
os.system("rm -rf amp_scan.cal")
gaincal(vis=vis+"_bpcal.ms",
        caltable="amp_scan.cal",
        field="0,2,3",
        solint="inf",
        calmode="a",
        refant="DV22",
        gaintype="G",
        gaintable=["phase_int.cal"])

# -------------------
# APPLICATION
# -------------------

# scan based applied to everything
applycal(vis=vis+"_bpcal.ms",
         gaintable=["phase_scan.cal",
                    "amp_scan.cal"],
         interp=["linear",
                 "linear"],
         gainfield=[[],[]],
         applymode='calonly')
