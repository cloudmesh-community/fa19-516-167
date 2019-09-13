# fa19-516-167
# E.Cloudmesh.Common.5
# Objective: Develop a program that demonstartes the use of cloudmesh.common.StopWatch
# Note: error in book: module 'os' has no attribute 'sleep'

# Imports
from cloudmesh.common.StopWatch import StopWatch
import time
import math

# Start timer
StopWatch.start("pie_stopwatch")

# Wait for pie (3.1415926535) seconds
time.sleep(math.pi)

# Stop timer
StopWatch.stop("pie_stopwatch")

# Print results
print (StopWatch.get("pie_stopwatch"))