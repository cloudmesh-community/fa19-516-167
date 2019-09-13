# fa19-516-167
# E.Cloudmesh.Shell.2
# Write a new command with your firstname as the command name.

import os

# Get current directory
pwd = Shell.execute('pwd')
print(pwd)

# Create custom command path
command_author = 'bill_screen'
cm_command_directory = pwd + '/' + 'cloudmesh-' + command_author

# Generate template directory
result = Shell.execute('cms', ['sys command generate ' + command_author])
print(result)

# Change local directory to cm_command_directory
os.chdir(cm_command_directory)

# Run the setup script for the custom command
result = Shell.execute('python', ['setup.py', 'install'])
print(result)