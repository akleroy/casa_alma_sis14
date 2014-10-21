# This script steps you through your first CASA task and a basic
# script.

# Start the lesson by running casapy from the command line

# Copy the data from the working directory
os.system("rm -rf sis14_twhya_uncalibrated.ms")
os.system("cp -r ../working_data/sis14_twhya_uncalibrated.ms .")

# A full guide on CASA basics are here
# http://casaguides.nrao.edu/index.php?title=Getting_Started_in_CASA

# Get a list of tasks
tasklist

# A similar overview of tasks
# http://casaguides.nrao.edu/index.php?title=What_is_CASA%3F

# Get more information on listobs by typing "help listobs"

# Look at the available inputs
inp(listobs)

# Set the visibility
# Review the now-modified inputs
inp(listobs)

# Run listobs
go

# Look at the logger to see the input

# An alternative approach; now output to a file
os.system("rm my_listfile.txt")
listobs(vis="sis14_twhya_uncalibrated.ms", listfile="my_listfile.txt")

# You can run system commands from casapy
os.system("ls")
os.system("more my_listfile.txt")

# You can also execute scripts of commands. These are run as though
# you had typed them in at the command line. Open "first_script.py" to
# look at an example of a script then run it using the following
# command.
execfile("first_script.py")
