# This lesson steps you through a realistic calibration workflow. You
# will start with the uncalibrated data. Then you will execute a
# calibration script. After you inspect the data - as in the last
# tutorial - you will apply some flagging and then rerun the
# calibration. At the end, we will split out the calibrated and
# flagged data for further imaging.

# Copy the data from the working directory
os.system("rm -rf sis14_twhya_uncalibrated.ms")
os.system("cp -r ../../working_data/sis14_twhya_uncalibrated.ms .")

# We run our calibration here via a script. Take a minute to look
# through the script and see how it works.

# Run the script before any flagging.

vis = "sis14_twhya_uncalibrated"
execfile("calibration_script.py")

# Now you would inspect the data, following the previous lession. Go
# back and review, or try a few of the same commands from that lesson.

# Here we apply the already worked-out flagging

# First flag the two antennas entirely.
flagdata("sis14_twhya_uncalibrated.ms",
         antenna="DV01,DV19")

# Now specify a scan range for DV20.
flagdata("sis14_twhya_uncalibrated.ms",
         antenna="DV20",
         scan="27~34")

# Finally, pick a field and a channel/spw range for Ceres.
flagdata("sis14_twhya_uncalibrated.ms",
         field="2",
         spw="0:124~130")

# After flagging problematic data we want to rerun the entire
# calibration with the problem data removed (those data could affect
# the calibration of other antennas, so that removing them will
# improve the overall data quality).

vis = "sis14_twhya_uncalibrated"
execfile("calibration_script.py")

# Finally, let's split out the calibrated, flagged data. These should
# now be ready for imaging.

os.system("rm -rf sis14_twhya_calibrated_and_flagged.ms")
split(vis="sis14_twhya_uncalibrated_bpcal.ms",
      outputvis="sis14_twhya_calibrated_and_flagged.ms",
      datacolumn="corrected",
      keepflags=False)


