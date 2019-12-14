
from cloudmesh.storagelifecycle.StorageABC import StorageABC
from cloudmesh.storagelifecycle.providers.aws.Provider import Provider as AwsProvider
from cloudmesh.storagelifecycle.providers.gcp.Provider import Provider as GCPProvider

class Provider(StorageABC):
    
    def __init__(self, service=None, config="~/.cloudmesh/cloudmesh.yaml"):
        '''Initializes the provider. The default parameters are read 
            from the configuration file that is defined in yaml format.

        :param service: The name of the provider as defined in the yaml file
        :param config: The location of the yaml configuration file
        '''        
        
        super(Provider, self).__init__(service=service, config=config)

        if self.service == "aws":
            self.provider = AwsProvider(service=service, config=config)
        elif self.service == "google":
            self.provider = GCPProvider(service=service, config=config)
        #Not Implemented
        #elif self.kind == "azure":
            #self.provider = AzureProvidder(service=service, config=config)


    def put(self, storage_provider, storage_bucket_name, lifecycle_rules):
        '''Sets lifecycle configuration rules for your bucket. If a 
            lifecycle configuration exists, it replaces it.
   
        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :param lifecycle_rules: (--expiry_in_days=NUM_DAYS | --lifecycle_config FILE)
        :returns: Instance of Provider
        '''    
        provider = self.provider.put(storage_provider, storage_bucket_name, lifecycle_rules)
        return provider

    def delete(self, storage_provider, storage_bucket_name):
        '''Deletes the lifecycle configuration defined for a bucket. 

        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :returns: Instance of Provider
        '''
        provider = self.provider.delete(storage_provider, storage_bucket_name)
        return provider

    def get(self, storage_provider, storage_bucket_name):
        '''Loads the lifecycle configuration defined for a bucket. 

        :param storage_provider: Name of the cloud service provider
        :param storage_bucket_name: Name of the storage bucket
        :returns: Instance of Provider
        '''      
        provider = self.provider.get(storage_provider, storage_bucket_name)
        return provider