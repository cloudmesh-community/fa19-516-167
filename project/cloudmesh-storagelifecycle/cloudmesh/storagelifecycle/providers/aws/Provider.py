# Generic/Built-in
import json
import logging
import os

# Owned
from cloudmesh.common.console import Console
from cloudmesh.configuration.Config import Config
from cloudmesh.storagelifecycle.StorageABC import StorageABC

# Other
import boto3
from botocore.exceptions import ClientError

class Provider(StorageABC):
    '''
    Encapsulates methods used to cost effectively manage the lifecycle
    of objects stored in a cloud service provider (CSP) throughout the
    objects' lifecycle.
    '''

    def __init__(self, service=None, config="~/.cloudmesh/cloudmesh.yaml"):
        '''Initializes the provider. The default parameters are read 
            from the configuration file that is defined in yaml format.

        :param name: The name of the provider as defined in the yaml file
        :param configuration: The location of the yaml configuration file
        '''
        super().__init__(service=service, config=config)

        # Load config values from cloudmesh.yaml
        self.config = Config()        
        self.credentails = self.config["cloudmesh"]["storage"][service]["credentials"]

        # Create client connection
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = self.credentails["access_key_id"],
            aws_secret_access_key = self.credentails["secret_access_key"],
            region_name = self.credentails["region"]
        )        

        # Basic lifecycle config template for setting expiry in days
        self.lifecycle_rule = {
            "Rules": [
                {
                    "ID": "Object Store Expiration Rule",
                    "Filter": {
                        "Prefix": ""
                    },
                    "Status": "Enabled",
                    "Expiration": {
                        "Days": ""
                    }
                }
            ]}


    def put(self, storage_provider, storage_bucket_name, args):
        '''Sets lifecycle configuration rules for your bucket. If a 
            lifecycle configuration exists, it replaces it.
   
        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :exception: Exception
        :returns: Result of operation as string
        '''
        result = {}
        try:

            # Load config file
            config_file = self.load_config_files(args)            

            # Invoke service
            result = self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=storage_bucket_name, 
                LifecycleConfiguration=config_file)

            # Debug
            Console.ok(json.dumps(result, indent=4, sort_keys=True))

        except ClientError as error:
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

            # Invoke service    
            result = self.s3_client.delete_bucket_lifecycle(Bucket=storage_bucket_name)

            # Debug
            Console.ok(json.dumps(result, indent=4, sort_keys=True))

        except ClientError as error:
            Console.error(error, prefix=True, traceflag=True)
            return False

        return result        

    
    def get(self, storage_provider, storage_bucket_name):
        '''Loads the lifecycle configuration defined for a bucket. 

        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :exception: Exception
        :returns: Result of operation as string
        '''

        try:

            # Invoke service
            result = self.s3_client.get_bucket_lifecycle_configuration(Bucket=storage_bucket_name)
    
            # Debug
            Console.ok(json.dumps(result, indent=4, sort_keys=True))

        except ClientError as error:
            if error.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                Console.warning(error.response['Error']['Code'])                
                return []
            else:
                # e.response['Error']['Code'] == 'NoSuchBucket', etc.
                Console.error(error, prefix=True, traceflag=True)
                return None            
        
        return result['Rules']


    def load_config_files(self, config_file_args):
        '''Loads config files based on user option (--expiry_in_days=NUM_DAYS | --lifecycle_config FILE) '''

        # Initialize dict
        config_file = {}

        try:

            if(config_file_args.expiry_in_days):
                # Update lifecycle config template     
                self.lifecycle_rule['Rules'][0]['Expiration']['Days'] = int(config_file_args.expiry_in_days)
                config_file = self.lifecycle_rule
            else:
                # Get full path to config file 
                config_file_uri = os.path.expanduser(config_file_args.lifecycle_config)
                # Open file, read contents, convert string to dict, implicitly close file
                with open(config_file_uri, 'r') as json_file:
                    config_file = json.load(json_file)

                print(config_file)
        except Exception as error:
            Console.error(error, prefix=True, traceflag=True)        

        return config_file        