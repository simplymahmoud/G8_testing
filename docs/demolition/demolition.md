## Demolition Testing

This section describes the tests that test the behaviour of the system when critical components fail.

### Compute

#### Remove Compute Node
| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Power off 1 CPU Node | CPU Node goes in alarm in the healthcheck|
| VM's failing on failed CPU Node   | Recreate VM's from snapshots on different CPU node | VM's back up and running|
| Powered off CPU Node  | xxx | VM's back up and running|

@TODO describe how VM's come back up on other host

#### Failure scenarios for power supply
| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Take out A or B feed | System continues to function|
| Working system with one feed failing   | Put feed back in | System back in full redundant mode|

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Take out A AND B feed | CPU Node goes in alarm in the healthcheck|
After that - same as section on Remove Compute Node

#### Failure in networking

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Take out one of the 2 cables to the Mellanox switches | System continues to function |
| Working system with one cable failing   | Put cable back in | System back in full redundant mode|

### Storage

#### Remove Storage Node
| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's with associated disks deployed on each of the CPU Nodes, a snapshot for each of the VM's | Physically remove one server from the Storage Node | System continues to function |

@TODO - describe behaviour and describe actions to get back live.

#### Failure scenarios for disks in backend system
We assume the parity for the backend is (16:4) meaning 4 disks can fail out of 20.

You will have to deploy the OVS monitoring tools - see https://openvstorage.gitbooks.io/ovs-monitoring/content/docs/deploy_with_ansible.html

##### Failing 1 disks

Execute this for all tiers configured in the system.

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's with associated disks deployed on each of the CPU Nodes, make sure that rebalancing of the nodes is finished and all disks are with full parity | Physically remove one HDD/SSD from the storage node| System continues to function, all VM's have full access to their vDISKS, rebalancing starts to restore parity in the storage node |

##### Failing 2 disks
Execute this for all tiers configured in the system.

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's with associated disks deployed on each of the CPU Nodes, make sure that rebalancing of the nodes is finished and all disks are with full parity | Physically remove two HDD/SSD from the storage node| System continues to function, all VM's have full access to their vDISKS, rebalancing starts to restore parity in the storage node |

##### Failing 4 disks
Execute this for all tiers configured in the system.

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's with associated disks deployed on each of the CPU Nodes, make sure that rebalancing of the nodes is finished and all disks are with full parity | Physically remove four HDD/SSD from the storage node| System continues to function, all VM's have full access to their vDISKS, rebalancing starts to restore parity in the storage node |

##### Failing 5 disks
Execute this for all tiers configured in the system.

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's with associated disks deployed on each of the CPU Nodes, make sure that rebalancing of the nodes is finished and all disks are with full parity | Physically remove five HDD/SSD from the storage node| Healthchecker provides alarm indicating which vDISKS have been hit by the failure |

@TODO how do you recover from this ?

#### Failure scenarios for power supply
| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Take out A or B feed from the storage node | System continues to function|
| Working system with one feed failing   | Put feed back in | System back in full redundant mode|

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Take out A AND B feed | Storage Node goes in alarm in the healthcheck|
After that - same as section on Remove Storage Node

#### Failure in networking

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Take out one of the 2 cables to the Mellanox switches from the Storage Node| System continues to function |
| Working system with one cable failing   | Put cable back in | System back in full redundant mode|

### Networking

| Input        | Test Scenario           | Output  |
| ------------- |:-------------:| -----:|
| A fully healthy system (check on healthcheck), a few VM's deployed on each of the CPU Nodes, a snapshot for each of the VM's | Power off a full Mellanox switch | System continues to function |
| Working system with one Mellanox  | xxx | System back in full redundant mode|

@TODO add what needs to be done to recover from the situation
