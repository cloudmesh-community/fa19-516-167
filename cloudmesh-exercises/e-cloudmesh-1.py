# fa19-516-167 E.Cloudmesh.Common.1
# Objective: Develop a program that demonstartes the use of banner, HEADING, and VERBOSE

# Import CM console package
from cloudmesh.common.console import Console

# Test different types of CM logs messages
msg = "This is a test message"
Console.ok(msg) # prins a green message
Console.error(msg) # prins a red message proceeded with ERROR
Console.msg(msg) # prins a regular black message
Console.error(msg, prefix=True, traceflag=True)

# ----------

# Import CM utility package to display banner in console
from cloudmesh.common.util import banner

# Create banner text to display
banner("Cloud Computing E516 | Bill Screen | Fall 2019")

# ----------

# Import CM utility package to display heading in the console
from cloudmesh.common.util import HEADING

# Create module heading for this file
HEADING()
print ("Cloud Computing E516 | Bill Screen | Fall 2019")

# ----------

# Import debug package to create verbose log output
from cloudmesh.common.debug import VERBOSE

# Create sample verbose log output
key_value = {"Registry": "NCC-1701-D"}
VERBOSE(key_value)
