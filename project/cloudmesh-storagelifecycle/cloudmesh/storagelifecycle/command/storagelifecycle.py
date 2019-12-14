from __future__ import print_function
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.storagelifecycle.Provider import Provider
from cloudmesh.storagelifecycle.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE

class StoragelifecycleCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_storagelifecycle(self, args, arguments):
        """
        ::
        Usage:
            storagelifecycle put SERVICE STORAGE_BUCKET_NAME (--expiry_in_days=NUM_DAYS | --lifecycle_config FILE)
            storagelifecycle get SERVICE STORAGE_BUCKET_NAME            
            storagelifecycle delete SERVICE STORAGE_BUCKET_NAME 

        Options:
            --expiry_in_days=NUM_DAYS   Days until objects in bucket are removed
            --lifecycle_config FILE     File containing storage lifecycle rules for bucket or objects in bucket

        Arguments:
            SERVICE                 Name of the cloud service provider (i.e. aws, gcp, azure)
            STORAGE_BUCKET_NAME     Id of the cloud service provider bucket
            NUM_DAYS                NUMBER OF DAYS

        Description:
            Manage cloud service provider objects so that they are stored cost-effectively throughout their lifecycle.
            AWS and GCP are currently supported.
    
            storagelifecycle put SERVICE STORAGE_BUCKET_NAME (--expiry_in_days=NUM_DAYS | --lifecycle_config FILE)
                Creates a new lifecycle configuration for the bucket or replaces an existing lifecycle configuration.
        
            storagelifecycle delete SERVICE STORAGE_BUCKET_NAME
                Removes all the lifecycle configuration rules in the lifecycle subresource associated with the (STORAGE_ID).
        
            storagelifecycle get SERVICE STORAGE_BUCKET_NAME
                Returns the lifecycle configuration information set on the bucket.

        Example:
            storagelifecycle put "gcp" "cloudmesh-bucket-001" --expiry_in_days=90
            storagelifecycle put "gcp" "cloudmesh-bucket-001" --lifecycle_config="C:\\mydir\\gcp_lifecycle_config.json"                        
            storagelifecycle get "gcp" "cloudmesh-bucket-001"
            storagelifecycle delete "gcp" "cloudmesh-bucket-001"
        """

        # Map parameters with -- to regular argument dicts for easier processing.
        map_parameters(arguments,
                       "expiry_in_days",
                       "lifecycle_config")

        # Create instance of generic Provider service
        provider = Provider(arguments.SERVICE)

        # Invoke function based on command arguments
        if arguments["put"]:
            provider.put(arguments.SERVICE, arguments.STORAGE_BUCKET_NAME, arguments)
        elif arguments["get"]:
            provider.get(arguments.SERVICE, arguments.STORAGE_BUCKET_NAME)            
        elif arguments["delete"]:
            provider.delete(arguments.SERVICE, arguments.STORAGE_BUCKET_NAME)
        else:
            return NotImplementedError
        
        pass