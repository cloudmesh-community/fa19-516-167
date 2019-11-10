"""
Execute tests for GCP Storage Lifecycle Policy services. 

Using --durations switch to measure test execution time
>> py.test -v -s -W ignore::DeprecationWarning --durations=10

NOTE: need to install gsutil prior to execution --> pip install gsutil

"""
import os
import pytest
import json
import random
import boto3
from cloudmesh.common.Shell import Shell
from cloudmesh.configuration.Config import Config
from cloudmesh.compute.vm.Provider import Provider

class TestStorageLifecycleGCP(object):

    @classmethod 
    def setup_class(self):
        "Runs once per class"

        # Create random Bucket Name (must be lowercase)
        self.storage_bucket = 'cloudmeshtest' + str(random.randint(10000, 100000))
        self.storage_lifespan = random.randint(1, 365)

        # Set constants
        self.GCP_PROJECT_ID = 'cloudmesh-storagelifecycle'        
        self.SERVICE_CLI = 'gsutil'
        self.STORAGE_BUCKET_PROTOCOL = 'gs://'
        self.SERVICE_COMMAND_CREATE_BUCKET = 'mb'
        self.SERVICE_COMMAND_REMOVE_BUCKET = 'rb'        
        self.SERVICE_SUBCOMMAND_GET = 'get'
        self.SERVICE_SUBCOMMAND_SET = 'set'
        self.GCP_PROJECT_ID_SWITCH = '-p'


    def test_create_storage_bucket(self):
        ''' Create Storage Bucket '''

        result = Shell.execute(self.SERVICE_CLI,
        [
            self.SERVICE_COMMAND_CREATE_BUCKET,
            self.GCP_PROJECT_ID_SWITCH,
            self.GCP_PROJECT_ID,                
            self.STORAGE_BUCKET_PROTOCOL + self.storage_bucket
        ])

        # Evaluate result        
        assert "Creating {0}".format(self.STORAGE_BUCKET_PROTOCOL + self.storage_bucket) in result


    def test_create_storage_lifecycle_policy(self):
        ''' Create Storage Lifecycle Policy '''

        # Execute CMS command 
        result=Shell.execute("cms",["storagelifecycle","put","gcp",self.storage_bucket,
        "--expiry_in_days={0}".format(self.storage_lifespan)])
        
        # Evaluate result
        assert "Setting lifecycle configuration on {0}".format(self.STORAGE_BUCKET_PROTOCOL + self.storage_bucket) in result

    
    def test_get_storage_lifecycle_policy(self):
        ''' Return Storage Lifecycle Policy details '''

        # Execute CMS command 
        result = {}        
        result = json.loads(Shell.execute("cms",["storagelifecycle","get","gcp",self.storage_bucket]))

        # Evaluate result
        assert result["rule"][0]["condition"]["age"] == self.storage_lifespan


    def test_delete_storage_lifecycle_policy(self):
        ''' Delete Storage Lifecycle Policy '''

        # Execute CMS command 
        result=Shell.execute("cms",["storagelifecycle","delete","gcp",self.storage_bucket])

        # Evaluate result
        assert "Setting lifecycle configuration on {0}".format(self.STORAGE_BUCKET_PROTOCOL + self.storage_bucket) in result


    def test_delete_storage_bucket(self):
        ''' Delete Storage Bucket '''

        # Delete the bucket 
        result = Shell.execute(self.SERVICE_CLI,
        [
            self.SERVICE_COMMAND_REMOVE_BUCKET,
            self.STORAGE_BUCKET_PROTOCOL + self.storage_bucket
        ])

        # Evaluate result        
        assert "Removing {0}".format(self.STORAGE_BUCKET_PROTOCOL + self.storage_bucket) in result

    @classmethod
    def teardown_class(self):
        "Runs at end of class"        