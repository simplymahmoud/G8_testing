## UnixBench Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have admin access to one of the physical compute nodes

### Test case description
- Create an account
- Create a number of cloud spaces that will be used for the test
- Create a number of virtual machines you want to run the UnixBench on
- Install UnixBench on the created virtual machines
- Run UnixBench on the first virtual machine and store its score
- Run UnixBench on all virtual machines, then store all UnixBench scores

### Expected result
- Create a result table providing the average UnixBench score per virtual machine:

  |VM name  | CPUs  | Memory | HDD | Iteration 1 | Iteration 2 | ... | Iteration x | Avg UnixBench Score|

### Running the test
- The test is divided into 2 scripts:

    - **2_unixbench_create_vms.py** creates all virtual machines and installs UnixBench on them
    - **2_unixbench_run.py** runs UnixBench on the specified number of virtual machines in parallel


- Go to the performance testing directory:

  ```
  cd /root/G8_testing/performance_testing
  ```

- Change the test parameters:

  ```
  vim Testsuite/2_Unixbench2_test/parameters.cfg
  ```

- Following parameters can be configured:

  ```  
  # Number of cloud spaces
  No_of_cloudspaces: 1

  # Full path of the directory where results should be outputted
  Res_dir: /root/G8_testing/tests_results/2_unixbench2

  # Number of VMs to be created for the test
  VMs: 2

  # Number of times UnixBench needs to run per VM
  unixbench_run_times: 1

  # Time difference (in secs) between starts of UnixBench tests on VMs
  vms_time_diff: 1

  # RAM specifications
  memory: 8192

  # Number of vCPU cores
  # Choose values in function of the RAM specifications [RAM, vCPUs]: [512,1], [1024,1], [4096,2], [2048,2], [8192,4] or [16384,8]
  cpus: 4

  # Boot Disk size (in GB)
  # Choose between these values: [10, 20, 50, 100, 250, 500, 1000, 2000]
  Bdisksize: 100
  ```

- Finally start creating virtual machines:

  ```
  jspython Testsuite/2_Unixbench2_test/2_unixbench_create_vms.py
  ```

- Then run UnixBench on a specified number of virtual machines, for instance here on 3 virtual machines, assuming 10 (for example) were created previously:

  ```
  jspython Testsuite/2_Unixbench2_test/2_unixbench_run.py 3
  ```

- To clean the test once completed:

 ```
  jspython scripts/tear_down.py unixbench2testuser
  ```

### Result sample
Results can be found in separate files:

```
cd G8_testing/tests_results/Unixbench_results/(date)_(cpu_name).(env_name)_testresults(run_number)/
vim (date)_(cpu_name).(env_name)_testresults(run_number).csv
```


![unixbench](https://cloud.githubusercontent.com/assets/15011431/14142022/b3a054de-f68b-11e5-8996-259aca0fba93.png)
