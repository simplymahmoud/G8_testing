
## FIO Settings
- FIO is a tool that will spawn a number of threads or processes doing a particular type of I/O action as specified by the user. The typical use of fio is to write a job file matching the I/O load one wants to simulate. 


- The FIO is a test that runs per specific disk. The command that is used here is excuted per each disk per vm and in a multiprocessing way which means we start running the same command on all disks per vm on the same time.

The command used:

`fio --ioengine=libaio --bs=4k --direct=1 --gtod_reduce=1 --iodepth=128  --name=test --size=1000M --readwrite=write --numjobs=3  --runtime=300 --directory=/mnt/disk_b`

Note: the default block size that is used here is 4k (bs=4k)

--ioengine=libaio --> for Linux native asynchronous I/O

--direct=1      --> means non buffered IO

--gtod_reduce=1   --> to reduce results for presenting only the important information

--iodepth=128  --> Number of I/O units to keep in flight against the file

--runtime=300 --> Limit run time to runtime seconds

--directory=/mnt/disk_b --> from where i will run the command (directory = where the disk is mounted)

--readwrite=write --> Type of I/O pattern (write means sequential write)

--size=1000M      --> the size of the file that will be written

--numjobs=3       --> Number of processes (in this case each process will wirte 1G which means When running the test we are writing 3GB of data per disk )

So this means if we have defined 5 disks per VM we will write 3GB x 5 disk for each iteration.
