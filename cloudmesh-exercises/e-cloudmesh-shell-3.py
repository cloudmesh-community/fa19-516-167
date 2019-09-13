# fa19-516-167
# E.Cloudmesh.Shell.3
# Write a new command and experiment with docopt syntax and argument 
# interpretation of the dict with if conditions.

from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand

class BillScreenCommand(PluginCommand):
  @command
  def do_bill_screen(self, args, arguments):
    """
    ::
    Usage:
      bill_screen -f FILE
      bill_screen list

    This command does some useful things.
      Arguments:
        FILE a file name
      Options:
      -f specify the file
    """
    print(arguments)
    if arguments.FILE:
      print("You have used file: ", arguments.FILE)
    return ""

# Invoke the do_bill_screen function
result = Shell.execute('cms', ['bill_screen', '-f', '\"file name with spaces\"'])
print(result)