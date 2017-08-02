## FIO Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have an admin user with only one corresponding account
- Make sure you JumpScale8 is installed on your personal machine; see the [JumpScale8 installation documentation](https://github.com/Jumpscale/jumpscale_core8/blob/master/docs/GettingStarted/Installation.md)


### Test description
- Create one user with one account
- Create the required number of cloud spaces
- Create the required number of virtual machines
  - The virtual machines will we spread over the number of nodes depending on the free resources
- Install **Flexible I/O** (FIO) tester tool (https://linux.die.net/man/1/fio)
- Run FIO on all virtual machines in parallel


### Running the test
- The actual test is divided into 2 scripts:

  - **add_vms.py** creates all virtual machines; these virtual machines are also used for running the UnixBench test, so no need to rerun this script if the machines were already created before
  - **run_fio.py** actually runs the FIO tests on all virtual machines in parallel

- So first you need to create the virtual machines using **add_vms.py**:

  ```
  cd G8_testing/performance_testing/scripts/
  python3 add_vms.py --{provide needed parameters}
  ```

  **Following parameters are available**:

  ```
  -u USERNAME, --user=USERNAME
                        username to login on the OVC api
  -p PASSWORD, --pwd=PASSWORD
                        password to login on the OVC api
  -e ENVIRONMENT, --env=ENVIRONMENT
                        environment to login on the OVC api
  -l LOCATION, --loc=LOCATION
                        location to create cloudspaces
  -c CLOUDSPACES, --clspcs=CLOUDSPACES
                        minimum number of cloudspaces
  -v VMACHINES, --vms=VMACHINES
                        minimum number of vmachines per cloudspace
  -i IMAGE, --img=IMAGE
                        image to use for creating vmachines
  -b BOOTDISK, --boot=BOOTDISK
                        bootdisk size
  -d DATADISK, --data=DATADISK
                        datadisk size
  -m MEMORY, --mem=MEMORY
                        amount of memory for the virtual machines
  -k CPU, --cpu=CPU     amount of vcpus for the virtual machines
  -o IOPS, --iops=IOPS  maximum of iops of the disks for the virtual machines
  -n CONCURRENCY, --con=CONCURRENCY
                        amount of concurrency to execute the job
  ```

- Then run the actual FIO test using **run_fio.py**:

  ```
  cd G8_testing/performance_testing/scripts
  python3 run_fio.py --{provide needed parameters}
  ```

  **Following parameters are available**:

  ```
  -u USERNAME, --user=USERNAME
                        username to login on the OVC api
  -p PASSWORD, --pwd=PASSWORD
                        password to login on the OVC api
  -e ENVIRONMENT, --env=ENVIRONMENT
                        environment to login on the OVC api
  -d DATA_SIZE, --ds=DATA_SIZE
                        Amount of data to be written per each data disk per VM
                        (in MB)
  -t TESTRUN_TIME, --run_time=TESTRUN_TIME
                         Test-rum time per virtual machine  (in seconds)
  -w WRITE_TYPE, --IO_type=WRITE_TYPE
                        Type of I/O pattern
  -m RWMIXWRITE, --mixwrite=RWMIXWRITE
                         Percentage of a mixed workload that should be writes
  -b BLOCK_SIZE, --bs=BLOCK_SIZE
                        Block size
  -i IODEPTH, --iodp=IODEPTH
                        number of I/O units to keep in flight against the file
  -o DIRECT_IO, --dio=DIRECT_IO
                        If direct_io = 1, use non-buffered I/O.
  -x RATE_IOPS, --max_iops=RATE_IOPS
                        Cap the bandwidth to this number of IOPS
  -j NUMJOBS, --numjobs=NUMJOBS
                         Number of clones (processes/threads performing the
                        same workload) of this job
  -f TYPE, --fs=TYPE    Use disk as a block device or make it use the
                        filesystem, choice are 'filesystem' or 'blkdevice'
  -v REQUIRED_VMS, --vms=REQUIRED_VMS
                         selected number of virtual machines to run fio on
  -r RESULTS_DIR, --rdir=RESULTS_DIR
                        absolute path fot results directory
  -n CONCURRENCY, --con=CONCURRENCY
                        amount of concurrency to execute the job
  -s TESTSUITE, --ts=TESTSUITE

  ```

- You can rerun **run\_fio.py** as many times as needed, using different parameters


### Check the test results
- The results of the tests will on the results directory specified during the test:

  ```
  cd (results_directory)/(date)_(cpu_name).(env_name)_testresults(run_number)/
  vim (date)_(cpu_name).(pc_hostname)_testresults(run_number).csv
  ```

- Also results will be pushed on the environment repo under **testresults** directory

  - In order to make this work make sure to identify who you are:

  ```
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
  ```
  - Also make sure to have your ssh key on the machine that will be used for running the test. And that you 
    have access on the environment repo where the results will be pushed.

- In the test result file we can view the following information:
  - Total IOPS per virtual machine per iteration
  - Average CPU load

- For each run of the **run\_fio.py**, there is a separated folder that is created which has its own CSV file

### Tearing Down the test
 - In order to clean all the created virtual machines and deployed cloud spaces:
 
  ```
  cd G8_testing/performance_testing/scripts
  python3 cleanup_vms.py --{provide needed parameters}
  ```

  **Following parameters are available**:
  ```
  -u USERNAME, --user=USERNAME
                        username to login on the OVC api
  -p PASSWORD, --pwd=PASSWORD
                        password to login on the OVC api
  -e ENVIRONMENT, --env=ENVIRONMENT
                        environment to login on the OVC api
  -n CONCURRENCY, --con=CONCURRENCY
                        amount of concurrency to execute the job
  ```
