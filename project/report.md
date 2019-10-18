# Cloudmesh Virtual Directory Life Cycle Service

Bill Screen

## Abstract

TBD

## Objective

Integrate Cloudmesh with cloud service providers' object storage lifecycle management services to 
effectively manage storage costs throughout their lifecycle. This service is intended to be added 
to the Cloudmesh storage project https://github.com/cloudmesh/cloudmesh-storage 
Implementation of lifecycle policies will be provided for AWS and Azure cloud providers, and locally if time permits.

## Motivation

As the volume of data being generated and stored by cloud service providers (CSP) continues 
to grow, the cost to store the data needs to be managed in a thoughtful manner. Without a 
data lifecycle management strategy, objects sent to a CSP could be stored indefinitely; even 
if the objects (data) are infrequently or never accessed, the customer will likely be charged 
for storage (beyond a certain 'free storage limit'). Thus applying a lifecycle storage policy will 
help to mitigate cost overruns by applying 'lifecycle rules' to efficiently manage objects stored in 
the cloud. For example, a lifecycle rule may schedule an object for deletion after 30 days or automatically
move the object to a lower-cost storage tier after 90 days.

 
## Architecture

TBD

## Technologies

* cloudmesh storage
* OpenAPI 3.0.2
* REST
* MongoDB (if time permits) 
 
```
Usage:

    storage_lifecycle_configuration [--storage_provider=<SERVICE>] put lifecycle_rules STORAGE_BUCKET_ID, LIFECYCLE_RULES
    storage_lifecycle_configuration [--storage_provider=<SERVICE>] delete lifecycle_rules STORAGE_BUCKET_ID, LIFECYCLE_RULES
    storage_lifecycle_configuration [--storage_provider=<SERVICE>] get_available_subresources STORAGE_BUCKET_ID
    storage_lifecycle_configuration [--storage_provider=<SERVICE>] load lifecycle_rules STORAGE_BUCKET_ID

Arguments:
    STORAGE_BUCKET_ID: Unique identifier of the storage bucket
    LIFECYCLE_RULES: An XML document used to specify the lifecycle of the STORAGE_ID. For example:

    <LifecycleConfiguration>
        <Rule>
            <ID>id2</ID>
            <Filter>
                <Prefix>my_logs/</Prefix>
            </Filter>
            <Status>Enabled</Status>
            <Expiration>
                <Days>365</Days>
            </Expiration>
        </Rule>
    </LifecycleConfiguration>
    
Options:
  -h --help
  --storage_provider=<SERVICE> Cloud storage provider service name (i.e. aws, azure, google, box)

Description:
    Manage Amazon S3 objects so that they are stored cost-effectively 
    throughout their lifecycle.

    storage_lifecycle_configuration put lifecycle_rules
        Creates a new lifecycle configuration for the bucket (STORAGE_ID) 
        or replaces an existing lifecycle configuration.

    storage_lifecycle_configuration delete lifecycle_rules
        Deletes the lifecycle configuration from the specified bucket 
        (STORAGE_ID). Removes all the lifecycle configuration rules in the 
        lifecycle subresource associated with the (STORAGE_ID).

    storage_lifecycle_configuration get_available_subresources
        Returns a list of all the available sub-resources for this Resource.

    storage_lifecycle_configuration load
        Returns the lifecycle configuration information set on the bucket.

Example:
    set storage_provider=aws|azure
    storage_lifecycle_configuration put STORAGE_BUCKET_ID, LIFECYCLE_RULES
```

## Progress

**Week of 10/06:** After many struggles, finally got Cloudmesh and MongoDB to install on Windows 10 (call 'cms init' twice!). Automated the install process via a batch script. Also added logic to validate connectivity to chameleon Cloud by executing 'image' and 'flavor' list commands. 

**Week of 10/13:** Reviewing the cloudmesh storage source code to understand the Python coding design pattern to follow for this project. Also trying to understand how to use VS Code debugger with CM source code, and how to setup pytests. 

 
