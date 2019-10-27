#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Futures
from __future__ import unicode_literals
from __future__ import print_function

# Generic/Built-in
import json
import logging
import os

# Owned
from cloudmesh.common.console import Console
from cloudmesh.configuration.Config import Config
from cloudmesh.common3.Shell import Shell
from cloudmesh.storage.StorageABC import StorageABC

class Provider(StorageABC):
    '''
    Encapsulates methods used to cost effectively manage the lifecycle
    of objects stored in a cloud service provider (CSP) throughout the
    objects' lifecycle.

    NOTE: for initial (one-time) authentication with GCP, 
    you MUST RUN 'gsutil config' and follow the instructions!
    It will create this file: 'C:\\Users\\myusername\\.boto'
    '''

    def __init__(self, service=None, config="~/.cloudmesh/cloudmesh.yaml"):
        '''Initializes the provider. The default parameters are read 
            from the configuration file that is defined in yaml format.

        :param name: The name of the provider as defined in the yaml file
        :param configuration: The location of the yaml configuration file
        '''
        super().__init__(service=service, config=config)
        self.config = Config()

        # Set constants
        self.SERVICE_CLI = 'gsutil'        
        self.STORAGE_BUCKET_PROTOCOL = 'gs://'
        self.SERVICE_COMMAND_LIFECYCLE = 'lifecycle'
        self.SERVICE_SUBCOMMAND_GET = 'get'
        self.SERVICE_SUBCOMMAND_SET = 'set'
        self.SERVICE_CONFIG_FILE = r"~\.cloudmesh\cloudmesh_gcp_storage_lifecycle.json"
        self.SERVICE_CONFIG_FILE_FOR_DELETES = r"~\.cloudmesh\cloudmesh_gcp_storage_lifecycle_empty.json"        

        # Basic lifecycle config template for setting expiry in days
        self.lifecycle_rule = {
            "lifecycle": {
            "rule": [{
                "action": {"type": "Delete"},
                "condition": {
                "age": "{days}",
                "isLive": True
                }
            }]}
        }

        # Empty JSON file for removing storage lifecycle rules
        self.lifecycle_rule_for_deletes = {}      

    def put(self, storage_provider, storage_bucket_name, args):
        '''Sets lifecycle configuration rules for your bucket. If a 
            lifecycle configuration exists, it replaces it.
   
        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :exception: Exception
        :returns: Result of operation as string
        '''

        try:
            # Load config file
            config_file = self.load_config_files(args)

            # Invoke GCP gsutil via CMS command shell
            result = Shell.execute(self.SERVICE_CLI,
            [
                self.SERVICE_COMMAND_LIFECYCLE,
                self.SERVICE_SUBCOMMAND_SET,
                config_file,                
                self.STORAGE_BUCKET_PROTOCOL + storage_bucket_name
            ])

            # Cleanup
            if(args.expiry_in_days):
                os.remove(config_file)

            # Debug
            Console.ok(result)

        except Exception as error:
            Console.error(error, prefix=True, traceflag=True)
        
        return result

    def delete(self, storage_provider, storage_bucket_name):
        '''Deletes the lifecycle configuration defined for a bucket. 

        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :exception: Exception
        :returns: Result of operation as string
        '''

        try:

            # Create storage lifecycle config files if doesn't exist
            self.create_lifecycle_config_files(
                config_path=self.SERVICE_CONFIG_FILE_FOR_DELETES, 
                config_file_data=self.lifecycle_rule_for_deletes)  

            # Set shell-like path expansion
            config_file = os.path.expanduser(self.SERVICE_CONFIG_FILE_FOR_DELETES)

            # Invoke GCP gsutil via CMS command shell
            result = Shell.execute(self.SERVICE_CLI,
            [
                self.SERVICE_COMMAND_LIFECYCLE,
                self.SERVICE_SUBCOMMAND_SET,
                config_file,                
                self.STORAGE_BUCKET_PROTOCOL + storage_bucket_name
            ])

            # Cleanup 
            os.remove(config_file)

            # Debug
            Console.ok(result)

        except Exception as error:
            Console.error(error, prefix=True, traceflag=True)
        
        return result
    
    def get(self, storage_provider, storage_bucket_name):
        '''Loads the lifecycle configuration defined for a bucket. 

        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :exception: Exception
        :returns: Result of operation as string
        '''

        try:
            # Invoke GCP gsutil via CMS command shell
            result = Shell.execute(self.SERVICE_CLI,
            [
                self.SERVICE_COMMAND_LIFECYCLE,
                self.SERVICE_SUBCOMMAND_GET,
                self.STORAGE_BUCKET_PROTOCOL + storage_bucket_name
            ])

            # Debug
            Console.ok(result)

        except Exception as error:
            Console.error(error, prefix=True, traceflag=True)
        
        return result

    def create_lifecycle_config_files(self, config_path, config_file_data):
        '''Creates lifecycle config files'''

        try:
            # Get file path
            service_config_file = os.path.expanduser(config_path)
            
            # Create config file in .cloudmesh directory
            f = open(service_config_file, 'w')  # Opens in write-only mode
            f.write(json.dumps(config_file_data))
            f.close()

            # Debug
            Console.ok("Successfully created temp config file in .cloudmesh directory")

        except Exception as error:
            Console.error(error, prefix=True, traceflag=True)        

        return

    def load_config_files(self, config_file_args):
        '''Loads config files based on user option (--expiry_in_days=NUM_DAYS | --lifecycle_config FILE) '''

        config_file = ""

        try:

            if(config_file_args.expiry_in_days):
                # Update lifecycle config template 
                self.lifecycle_rule['lifecycle']['rule'][0]['condition']['age'] = config_file_args.expiry_in_days
                
                # Dynamically generate lifecycle config file for gsutil         
                self.create_lifecycle_config_files(config_path=self.SERVICE_CONFIG_FILE, config_file_data=self.lifecycle_rule)

                # Set shell-like path expansion for config file
                config_file = os.path.expanduser(self.SERVICE_CONFIG_FILE)
            else:
                # Set shell-like path expansion for config file
                config_file = os.path.expanduser(config_file_args.lifecycle_config)                

        except Exception as error:
            Console.error(error, prefix=True, traceflag=True)        

        return config_file