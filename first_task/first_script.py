# This is a comment

# A python command
print "Hello CASA!"

# A call to a system command
os.system("rm -rf my_script_listfile.txt")

# A CASA command
listobs(vis="sis14_twhya_uncalibrated.ms", listfile="my_script_listfile.txt")


