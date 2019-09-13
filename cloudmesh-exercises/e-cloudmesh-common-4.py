# fa19-516-167
# E.Cloudmesh.Common.4
# Objective: Develop a program that demonstartes the use of cloudmesh.common.Shell.

# Imports
from cloudmesh.common.Shell import Shell

# ps shows process status
result = Shell.execute('ps', ["-ef"]) # Note: error in book, 'result' is not defined
print(result)

# env allows you to set or print the environment variables.
result = Shell.execute('env')
print(result)