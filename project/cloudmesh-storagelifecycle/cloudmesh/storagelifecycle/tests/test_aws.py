"""
Execute tests for AWS Storage Lifecycle Policy services. 

Using --durations switch to measure test execution time
>> py.test -v -s -W ignore::DeprecationWarning --durations=10

"""

import pytest
import json
import random
import boto3
from cloudmesh.common.Shell import Shell
from cloudmesh.configuration.Config import Config
from cloudmesh.compute.vm.Provider import Provider
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark

class TestStorageLifecycleAWS(object):

    @classmethod 
    def setup_class(self):
        "Runs once per class"

        # Create random Bucket Name (must be lowercase)
        self.storage_bucket = "cloudmeshtest" + str(random.randint(10000, 100000))
        self.storage_lifespan = random.randint(1, 365)

        # Load config values from cloudmesh.yaml
        self.config = Config()        
        self.credentails = self.config["cloudmesh"]["storage"]["aws"]["credentials"]
        self.storage = "aws"

        # Create client connection
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = self.credentails["access_key_id"],
            aws_secret_access_key = self.credentails["secret_access_key"],
            region_name = self.credentails["region"]
        ) 


    def test_create_storage_bucket(self):
        ''' Create Storage Bucket '''

        HEADING()
        Benchmark.Start()

        # Create the bucket (must be globally unique name)
        result = self.s3_client.create_bucket(Bucket=self.storage_bucket)

        # Evaluate result
        json.dumps(result)
        assert result["ResponseMetadata"]["HTTPStatusCode"] == 200

        Benchmark.Stop()        

    def test_create_storage_lifecycle_policy(self):
        ''' Create Storage Lifecycle Policy '''
        
        HEADING()
        Benchmark.Start()

        # Execute CMS command 
        result=Shell.execute("cms",["storagelifecycle","put","aws",self.storage_bucket,
        "--expiry_in_days={0}".format(self.storage_lifespan)])

        # Evaluate result
        data = json.loads(result)
        assert data["ResponseMetadata"]["HTTPStatusCode"] == 200

        Benchmark.Stop()        
     
    def test_get_storage_lifecycle_policy(self):
        ''' Return Storage Lifecycle Policy details '''

        HEADING()
        Benchmark.Start()

        # Execute CMS command 
        result=Shell.execute("cms",["storagelifecycle","get","aws",self.storage_bucket])

        # Evaluate result
        data = json.loads(result)
        assert data["ResponseMetadata"]["HTTPStatusCode"] == 200

        Benchmark.Stop()        
    
    def test_delete_storage_lifecycle_policy(self):
        ''' Delete Storage Lifecycle Policy '''
        
        HEADING()
        Benchmark.Start()

        # Execute CMS command 
        result=Shell.execute("cms",["storagelifecycle","delete","aws",self.storage_bucket])

        # Evaluate result (Successful delete = 204)
        data = json.loads(result)
        assert data["ResponseMetadata"]["HTTPStatusCode"] == 204        

        Benchmark.Stop()        

    def test_delete_storage_bucket(self):
        ''' Delete Storage Bucket '''

        HEADING()
        Benchmark.Start()

        # Delete the bucket 
        result = self.s3_client.delete_bucket(Bucket=self.storage_bucket)

        # Evaluate result
        json.dumps(result)
        assert result["ResponseMetadata"]["HTTPStatusCode"] == 204

        Benchmark.Stop()        

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=self.storage)    

    @classmethod
    def teardown_class(self):
        "Runs at end of class"        