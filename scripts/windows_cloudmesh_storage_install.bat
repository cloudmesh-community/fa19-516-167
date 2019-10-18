@echo off

:: ----------------------------------------------------------------------------------------------------
:: Purpose: Install Cloudmesh Storage package. This script will install Cloudmesh Storage, MongoDb, and generate 
:: a plugin directory on Windows OS
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
:: Change tp the cloudmesh workspace directory
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
:: Update your .yaml file
:: --------------------------------------------------

:: Cloudmesh attributes
:: --------------------------------------------------
cms config set cloudmesh.profile.firstname=myfirstname
cms config set cloudmesh.profile.lastname=mylastname
cms config set cloudmesh.profile.email="myusername@iu.edu"
cms config set cloudmesh.profile.user=myusername
cms config set cloudmesh.profile.github=mygithubusername

:: Lesson learned -- double quote backslashes on Windows
:: To find this key go to OpenStack- > Access & Security -> Key Pairs -> Your_Key -> Key Pair Details -> Public Key
:: Looks like: ssh-rsa AAAAB3NzaC................. Generated-by-Nova
cms config set cloudmesh.profile.publickey="C:\\Users\\bscreen\\my_ssh_keys\\chamelon_openstack_id_rsa.pub"

:: MongoDb attributes
:: --------------------------------------------------
cms config set cloudmesh.data.mongo.MONGO_USERNAME=admin
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=mypassword
cms config set cloudmesh.data.mongo.MONGO_AUTOINSTALL=True

:: Chameleon cloud attributes
:: --------------------------------------------------
cms config set cloudmesh.cloud.chameleon.credentials.OS_USERNAME=myusername
cms config set chameleon.cloud.chameleon.credentials.OS_PASSWORD="mypassword"
cms config set chameleon.cloud.chameleon.credentials.OS_KEY_PATH="C:\\Users\\bscreen\\my_ssh_keys\\chamelon_openstack_id_rsa.pub"

:: Check the .yaml file 
cms config check

:: --------------------------------------------------	
:: Install MongoDB
:: Note: For Windows10 press the [Ignore] button for this error: 
:: Service 'MongoDB Server (MongoDB) failed to start. Verify that you have sufficient priviledges to start system services.'
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
:: Remove plugin directory (no longer needed)
:: --------------------------------------------------
rmdir /s /q  mycommand\cloudmesh-mycommand\cloudmesh\plugin

:: --------------------------------------------------	
:: Install mycommand
:: --------------------------------------------------
pip install -e mycommand\cloudmesh-mycommand

:: --------------------------------------------------	
:: Test running mycommand with and without params
:: --------------------------------------------------
cms mycommand --file "c:\\mydir\\myfile.txt"
cms mycommand list

:: --------------------------------------------------	
:: Open Visual Studio Code in this directory
:: --------------------------------------------------
code .
