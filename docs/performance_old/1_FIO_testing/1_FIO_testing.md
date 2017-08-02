## FIO Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have admin access to one of the physical compute nodes

### Test description
-  Create a user:
  - username: perftestuser
  - password: gig12345
- Create a cloud space, with a randomly generated name
- Create the required number of virtual machines
  - The virtual machines will we spread over the number of nodes you indicated in **Perf_parameters.cfg**
  - The names of the virtual machines are formatted as "nodex_y", where x is the ID of the node (stack) and y is the number of the virtual machine
- Install **Flexible I/O** (FIO) tester tool and create and mount the data disks 
- Make sure to update **Perf_parameters.cfg** with the parameters needed


### Running the test
- Prior to running the script make sure that the environment is clean, using the **tear_down.py** script:

  ```
  cd G8_testing/performance_testing
  jspython scripts/tear_down.py --clean
  ```

- Then set the required parameters in **Perf_parameters.cfg**:

  ```
  cd G8_testing/performance_testing/Testsuite/1_fio_vms
  vim Perf_parameters.cfg
  ```

- Following parameters are settable in **Perf_parameters.cfg**:

```
# Number of Iterations --> each iteration create one VM per cpunode(stack)
iterations: 1

# No of cloudspaces 
No_of_cloudspaces: 1

# Number of cpu nodes which will be used for the test 
used_stacks: 2



# Parameters required for VM
# RAM and cpu are coupled together,
# please choose between these values [RAM, vcpu] = [512,1] or [1024,1] or [4096,2] or [2048,2] or [8192,4] or [16384,8]
# RAM specifications
memory: 2048
#vcpu cores
cpu: 2

#Boot Disk size (in GB), please choose between these values [10, 20, 50, 100, 250, 500, 1000, 2000] -- default = 100G
Bdisksize: 100

# Number of data disks per VM
no_of_disks: 1

# Data disksize per vm
data_disksize: 60

# Parameters required for FIO
# Block size
bs:4k
#IO depth:is the number of I/O units to keep in flight against the file.
iodepth: 1
#Direct IO: If direct_io = 1, use non-buffered I/O. Default:0
direct_io:0
#rwmixwrite: is the Percentage of a mixed workload that should be writes. If rwmixwrite = 70
#then rwmixread will be equal 30 by default
rwmixwrite:50

# FIO starting time difference between virtual machines (in seconds)
vms_time_diff: 1

# Test-rum time per virtual machine  (in seconds)
testrun_time: 300

# Amount of data to be written per each data disk per VM (in MB)
data_size: 4000

# Type of I/O pattern -- what you will enter will be the same for all VMs (enter:
# 'write' for sequential write or 'randwrite' for random write
# 'read' for sequential read or 'randread' for random read
# 'rw' for mixed sequential reads and writes or 'randrw' for mixed random reads and writes
# if you enter nothing then half of the vms will be write and the other half will be randwrite
IO_type: write

#rate_iops: Cap the bandwidth to this number of IOPS. Basically the same as rate, just specified independently of bandwidth
rate_iops: 8000

#numjobs: Number of clones (processes/threads performing the same workload) of this job. Default: 1.
numjobs:1


# Results Directory : write absolute directory
Res_dir: /root/G8_testing/tests_results/FIO_test

# username
username: perftestuser

# should run all scripts from inside the repo

```

- The actual test is divided into 2 scripts:
  - **demo\_create\_vms.py** creates all virtual machines
  - **demo\_run\_fio.py** actually runs the FIO tests on all virtual machines in parallel
- For instance in order to create 25 virtual machines and use 10 of the to run the test:

  ```
  cd G8_testing/performance_testing/
  jspython Testsuite/1_fio_vms/demo_create_vms.py 25
  jspython Testsuite/1_fio_vms/demo_run_fio.py 10 
  ```

- You can rerun **demo\_run\_fio.py** as many times as needed, using different parameters
- After finishing the test, make sure that the test environments is teared down using the **tear_down.py** specifying the user **perftestuser**:

  ```
  cd G8_testing/performance_testing
  jspython scripts/tear_down.py perftestuser 
  ```

### Check the test results
- The results of the tests are available in separate files:

  ```
  cd G8_testing/tests_results/FIO_test/(date)_(cpu_name).(env_name)_testresults(run_number)/
  vim (date)_(cpu_name).(env_name)_testresults(run_number).csv
  ```

- For each of the results there is also a copy available of the used **Perf_parameters.cfg** file:

  ```
  vim /G8_testing/tests_results/FIO_test/(date)_(cpu_name).(env_name)_testresults(run_number)/Perf_parameters.cfg
  ```

- In the test result file we can view the following information:
  - Total IOPS per virtual machine per iteration
  - Avergage CPU Load
  
- For each run of the **demo\_run\_fio.py**, there is a separated folder that is created which has its own CSV file and parameters file as discribed in the first point
