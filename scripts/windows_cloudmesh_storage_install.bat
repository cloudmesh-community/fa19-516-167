@echo off

:: ----------------------------------------------------------------------------------------------------
:: Purpose: This script is used to install Cloudmesh, MongoDb, and generate a plugin directory on Windows OS
:: Date: 2019-10-18
:: Author: wscreen
:: ----------------------------------------------------------------------------------------------------

:: --------------------------------------------------
:: Upgrade all Pip packages to the newest available version
:: --------------------------------------------------
python -m pip install --upgrade pip

:: --------------------------------------------------
:: Create the cloudmesh workspace directory
:: Note: Do NOT use the word 'cloudmesh' or an underscore '_'
:: --------------------------------------------------
mkdir cm

:: --------------------------------------------------
:: Change to the cloudmesh workspace directory
:: --------------------------------------------------
cd cm

:: --------------------------------------------------
:: Create a new virtual environment in the subdirectory
:: and configure the current shell to use it as the 
:: default python environment
:: --------------------------------------------------
python -m venv env3

:: --------------------------------------------------
:: Activate your virtualenv:
:: (e.g. (env3)Your-Computer:project_folder UserName$) 
:: lets you know that the virtual env is active.
:: Type: 'deactivate' to exit virtual environment
:: --------------------------------------------------
CALL .\env3\Scripts\activate

:: --------------------------------------------------
:: Clone your Github repo
:: --------------------------------------------------
git clone https://github.com/cloudmesh-community/fa19-515-167
git remote add origin https://github.com/cloudmesh-community/fa19-515-167.git

:: --------------------------------------------------
:: Install Cloudmesh Installer
:: --------------------------------------------------
pip install cloudmesh-installer

:: --------------------------------------------------
:: Clone and install CM repos
:: Note: this step will take ~8 minutes
:: --------------------------------------------------
cloudmesh-installer git clone storage
cloudmesh-installer git pull storage
cloudmesh-installer install storage -e

:: Validate the install worked
cms help

:: --------------------------------------------------	
:: Create ssh certs
:: --------------------------------------------------
:: cms key add my_username --source=ssh
:: cms key upload my_username --cloud=chameleon
:: cms set key my_username

:: --------------------------------------------------
:: Update your .yaml file
:: --------------------------------------------------

:: Cloudmesh attributes
:: --------------------------------------------------
cms config set cloudmesh.profile.firstname=TBD
cms config set cloudmesh.profile.lastname=TBD
cms config set cloudmesh.profile.email="TBD"
cms config set cloudmesh.profile.user=TBD
cms config set cloudmesh.profile.github=TBD

:: Lesson learned -- double quote backslashes on Windows
:: To find this key go to OpenStack- > Access & Security -> Key Pairs -> Your_Key -> Key Pair Details -> Public Key
:: Looks like: ssh-rsa AAAAB3NzaC................. Generated-by-Nova
cms config set cloudmesh.profile.publickey="TBD"

:: MongoDb attributes
:: --------------------------------------------------
cms config set cloudmesh.data.mongo.MONGO_USERNAME=TBD
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=TBD
cms config set cloudmesh.data.mongo.MONGO_AUTOINSTALL=True

:: Chameleon cloud attributes
:: --------------------------------------------------
cms config set cloudmesh.cloud.chameleon.credentials.OS_USERNAME=TBD
cms config set chameleon.cloud.chameleon.credentials.OS_PASSWORD="TBD"
cms config set chameleon.cloud.chameleon.credentials.OS_KEY_PATH="TBD"

:: Check the .yaml file 
cms config check

:: --------------------------------------------------	
:: Install MongoDB
:: Note: For Windows10 press the [Ignore] button for this error: 
:: Service 'MongoDB Server (MongoDB) failed to start. Verify that you
:: have sufficient priviledges to start system services.'
:: --------------------------------------------------
cms admin mongo install

:: --------------------------------------------------	
:: Call the Initialize method a few times (knwon issue)
:: https://cloudmesh.github.io/cloudmesh-manual/api/cloudmesh.init.command.html
:: --------------------------------------------------
cms init
cms init

:: --------------------------------------------------	
:: Test install by checking Chamelon cloud
:: --------------------------------------------------
cms config set cloud=chameleon
cms image list --refresh
cms flavor list --refresh

:: --------------------------------------------------	
:: Generate a folder for your project
:: --------------------------------------------------
mkdir mycommand
cd mycommand
cms sys command generate mycommand

:: --------------------------------------------------	
:: Install mycommand
:: --------------------------------------------------
pip install -e cloudmesh-mycommand

:: --------------------------------------------------	
:: Create some files for cloud provider implementation logic
:: --------------------------------------------------
type NUL >> cloudmesh-mycommand\cloudmesh\mycommand\Provider.py

mkdir cloudmesh-mycommand\cloudmesh\mycommand\providers\aws
type NUL >> cloudmesh-mycommand\cloudmesh\mycommand\providers\aws\Provider.py

mkdir cloudmesh-mycommand\cloudmesh\mycommand\providers\azure
type NUL >> cloudmesh-mycommand\cloudmesh\mycommand\providers\azure\Provider.py

mkdir cloudmesh-mycommand\cloudmesh\mycommand\providers\gcp
type NUL >> cloudmesh-mycommand\cloudmesh\mycommand\providers\gcp\Provider.py

:: C:.
:: └───cloudmesh-mycommand
::     ├───cloudmesh
::     │   ├───mycommand
::     │   │   ├───api
::     │   │   ├───command
::     │   │   ├───providers
::     │   │   │   ├───aws
::     │   │   │   ├───azure
::     │   │   │   └───gcp

:: --------------------------------------------------	
:: Test running mycommand
:: --------------------------------------------------
cms mycommand list

:: --------------------------------------------------	
:: Prefetch some certs you may need
:: --------------------------------------------------
:: WGET amazon cert ~/.cloudmesh/aws_cert.pem
:: WGET azure cert
:: WGET gcp cert

:: --------------------------------------------------	
:: Install Pytest
:: --------------------------------------------------
mkdir tests
pip install pytest

:: --------------------------------------------------	
:: Confirm Pytest install
:: --------------------------------------------------
py.test -h

:: --------------------------------------------------	
:: Open Visual Studio Code in this directory
:: --------------------------------------------------
code .

:: Uninstall
:: pip uninstall cloudmesh-mycommand