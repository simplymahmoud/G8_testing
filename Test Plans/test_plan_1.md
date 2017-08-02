# New features test plan (26 Oct 2016)
This is only a start plan which can be extended later on while more understanding each feature requirements.
 
Prepared by:
	(Ramez Saeed) 
	(26 Oct 2016)

## TABLE OF CONTENTS
    1.0  INTRODUCTION                         
    2.0  OBJECTIVES AND TASKS                         
        2.1  Objectives                                         
        2.2  Tasks                         
    3.0  SCOPE                                 
    4.0  Features to Be Tested     
    5.0  Testing Strategy                                                  
        5.1  System and Integration Testing                 
        5.2  Performance and Stress Testing                                                              
    6.0  Environment Requirements                                                                         
    7.0  Control Procedures                                                
    8.0  Resources/Roles & Responsibilities                                   
    9.0  Dependencies
    10.0  RISKS/ASSUMPTIONS
                                 
###1.0 INTRODUCTION
This test plan is a high level test overview for the mentioned new features,
more details about the test steps itself should be added in the future when have more info about
each feature and try them manually.
 
###2.0 OBJECTIVES AND TASKS
####2.1    Objectives
	create test coverage for all the mentioned new features.

####2.2    Tasks
	https://github.com/gig-projects/org_quality/issues/509

###3.0 SCOPE
	Functional testing
	Performance testing (@Geert: please provide which fields need to be tested and what/how is the expected result for them)

### 4.0 FEATURES TO BE TESTED
	1- Limit machine disk IOPS
	2- Resources management
	3- External networks
	4- AYS automatic snapshot
	5- AYS template for S3 
	6- AYS own cloud
	7- Import/Export machine features

### 5.0 TESTING STRATEGY
	we need to use the cockpit and AYS blue prints to drive test in these features.
	@Geert: please provide where we should add the test results as we used to track test results in jenkins but now for
			cockpit we need to have these result added somewhere (Ex.: push test results to github)
	
	## install cockpit
	- We need to install a stable cockpit somewhere to be used for drive test suites (Ex. be-scale-3)
		https://gig.gitbooks.io/cockpit/content/installation/installation.html

	## testing
	- we need to write the test which will be run through blue prints on the cockpit.
	There should be a configurable blue print which points out to the the environment to test.

	## AYS templates
	- For every script that we are running we need to create an AYS template. For the moment we have several AYS templates which can be re-used.

	## using REST APIs
	- this script can be used to call all the system REST APIs in order to check, verify and assert the results will come out from the blue prints:
		https://raw.githubusercontent.com/grimpy/openvcloudash/master/openvcloudash/openvcloud/client.py
		```
		client = Client(url, login, password)
		client.system.health.getOverallStatus()
		client.cloudapi.accounts.list()

		```
### 5.1    System and Integration Testing
	
	1- Limit machine disk IOPS:
		test1:
			1. create a blueprint to add (account, CS, VM) and deploy
			2. run fio test, store result
			3. edit blueprint to limit the IOPS of the VM and deploy
			4. run fio test, validate result against last deployed blueprint
			5. add a new disk to the VM in the blueprint, limit its IOPS and deploy
			6. run fio test, validate result against last deployed blueprint
			7. decrease the IOPS limits in the blueprint and deploy
			8. run fio test, validate result against last deployed blueprint
				
	2- Resources management
		Reference:
		https://github.com/0-complexity/selfhealing/blob/master/specs/resource-usage-tracking.md

		test1:
			create a blueprint to add (1 account, 2 CS, 4 VM)
			check what should be the time to wait until the bin file is created on master node
			download this bin file using API commands and assert all the info inside it are correct.
				this script can be used to read the bin file data:
				/opt/code/github/0-complexity/openvcloud/scripts/demo/export_account_xls.py
			add more VMs and check again
			expected result: all the data should be aggregated to the master node under directory has the name of the account ID.

		test2:
			test Upstream aggregation time (don't know how to do that yet, need to try it manually first)
		test3:
			do the same steps for destroyed/disabled accounts.
			Expected result: no more data aggregation should be done for destroyed/disabled accounts.

	
	3- External networks
		test1:
			test multiple networks for one cloud space (still need more info how to do that as there are no docs for this feature)
		test2:
			create an account with two different types of networks
			create a cloud space with specific network (pivate one)
			create two VMs and assert that they can talk to each other via the private network
		test3:
			test assign a network to specific account (@Jo: please update us with more info how we can do that)

	4- AYS automatic snapshot
		Reference Example:
			https://github.com/0-complexity/ays_vdc_automated_snapshots/blob/master/specs/vdc-automated-snapshots.md
		test1:
			create a template like the one in the example
			test the snapshot are created at the correct time (snapshotInterval) and assert they are there in the Env.
			test the snapshots are deleted at after the expire date (retentionScheme)
		test2:
			test all the fields in the AYS template (startdate, enddate, etc... )
			I think startdate: means the time for the snapshoting start to be done
				enddate: no more snapshots should be taken after that date
		test3:
			create 1 VM with snapshot interval 2 minutes
			after every snapshot write one file, do that at least two times
			restore the VM to the old create snapshots and assert that only the correct files are there

	5- AYS template for S3
		Reference:
			https://github.com/0-complexity/ays_s3_scality/blob/master/specs/initial.md
			https://github.com/0-complexity/ays_s3_scality/pull/1/files
		test1:
			Create AYS template with different combination of params and assert in the backend it had been reflected successfully.
				- **domain**=None, **maximum capacity**=None
				- **domain**=unexpected_domain, **maximum capacity**=None
				- **domain**=None, **maximum capacity**=unexpected_value
				- **domain**=value, **maximum capacity**=value
		test2:
			Test If **maximum capacity** is specified, the system will grow the storage dynamically until the **maximum capacity** is reached.
		test3:
			Test Dynamic storage capacity and assert in the backend it works exactly as described in the specs.
		test4:
			Assert for the result of blueprint deployment
			    - pub ipaddress
			    - access key
			    - secret key
		Note: @Azmy please provide us with more info and more expected test scenarios	

	6- AYS own cloud
		Reference:
			https://github.com/0-complexity/ays_owncloud/blob/master/specs/initial.md
			https://github.com/0-complexity/ays_owncloud/blob/master/specs/test_plan.md
		test1:
			
			Input parameters that customers will need to pass when buying an OwnCloud system
			[domain (optional), ItsYou.Online organization of people allowed to login, ItsYou.Online organization of people allowed to administer]
			create AYS blueprint template with different combination for the needed params
			assert that the passed params are reflected correctly in the created ownclod
			try to login/administer with not authenticated user
    		test2:
			test Dynamic storage capacity
		test3:
			test storage setup done correctly as described in the specs
			test Cockpit API results after deploying blueprint
			test export a VM to the deployed owncloud for the same VDC, should succeed
			create another ownclowd on different VDC
			test export a VM to the deployed owncloud for the different VDC, should fail

	7- Import/Export machine features
		Reference:
			https://github.com/0-complexity/openvcloud/blob/2.1/specs/import-export-virtual-machines.md
		test1:(import test)
			have access to owncloud so the test can import VMs
			create VM and upload ovf to owncloud
			on G8 Env try to import the uploaded Vm with all the needed params in the specs
			assert that G8 performs the import and sends results via email to the user

		test2: (export test)
			have access to owncloud so the test can export VMs
			on G8 Env try to export Vm with ID and path all the needed params in the specs
			assert that G8 performs the export and sends results via email to the user


### 5.2    Performance and Stress Testing
	1- Limit machine disk IOPS:
		Edit the performance existing FIO test to set the IOPS on disks and check the changes, expected that with each IOPS decrease the Env should handle more IOPS on different VMS.

	4- AYS automatic snapshot
		Load the environment with a lot of VMs
		put a small interval for automatic snapshot for all the VM
		start write to all the VMs and check the performance is affected by the snapshots running in background or not.
	6- AYS own cloud
		test load the owncloud (@Geert: need to know how we can load it, and what we should measure here)
		1. lots of storage: push over 5tb to the owncloud ==> expected result automatic scaling of the owncloud ays service kicks in and dynamically adds storage to the owncloud machine / btrfs /data filesystem
		   Hints:
		      create 100 mb random file
		      encrypt random file
		      encrypt encrypted random file
		      ...
		2. lots of clients: mount owncloud over webdav for 100, 1000, 10000 times and trigger filemodification on 10% of the mounts


### 6.0 ENVIRONMENT REQUIREMENTS
	1- Virtual machine to have the cockpit installed.
	2- test environment has all the new features installed and updated.
 
### 7.0 CONTROL PROCEDURES
	Problem Reporting
	@Geert: Please Document the procedures to follow when an incident is encountered during the testing 
		process and who is the goto person for each feature.

	Change Requests
	@Geert: Document the process of modifications to the software.  Identify who will sign off on the 
		changes and what would be the criteria for including the changes to the current product.  
  


### 8.0 RESOURCES/ROLES & RESPONSIBILITIES
	QA team members who are involved in this:
		Ramez Saeed
		Islam Taha

### 9.0 DEPENDENCIES
	- stable cockpit deployment and installation
	- stable AYS installation
	- support from the development team to help adding AYS templates as per tests requirements

### 10.0 RISKS/ASSUMPTIONS
	- Please note that there is maybe delay of delivery because of there is no knowledge about these new features
		in the testing team, so testing team will need some time for learning curve and manual tries for these features.
	- will use the new testing procedure which is running everything through cockpit and AYS which is not fully clear
		for the testing team yet.

