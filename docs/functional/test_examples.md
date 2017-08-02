## Report on using the OpenvCloud Test Suites

### How we tested

All tests have been started from a remote virtual machine on uk-g8-1: [Test Server of Yves](https://uk-g8-1.demo.greenitglobe.com/CBGrid/Virtual%20Machine?id=1405).

You can login to this machine with username `cloudscalers` and password `DCuf1T5rS`, but first make sure your private SSH key is loaded:

```
ssh-add -l
ssh cloudscalers@85.255.197.77 -p7922 -A
```

On the test server the Selenium Grid was installed, based on the [documentation](https://github.com/0-complexity/G8_testing/blob/selenium-hub-compatable/docs/functional/openvcloud/remote_machine_hosted/portal/portal.md)

Three tmux sessions were used for the tests:

```
tmux list-all sessions
```

The first two tmux sessions (`yves1` and `yves2`) have been used running two ACL and/or OVC tests simultaneously, while the third tmux session (`selenium`) was only used for the End User Portal tests.

For the End User Portal tests the `selenium-hub-compatable` branch of the [G8_testing](https://github.com/0-complexity/G8_testing) repository was cloned under `/opt/code/github/0-complexity/selenium`, while for the ACL and OVC tests allways the `master` branch was cloned in `opt/code/github/0-complexity/yves1` or `opt/code/github/0-complexity/yves2`.

By design the ACL and OVC tests will always run on the master node. Each time when a test is running the [G8_testing](https://github.com/0-complexity/G8_testing) repository will be cloned in `opt/code/{arbriatray-name}`. This clone gets automatically deleted once the test finishes.

Once an ACL or OVC test was started from the [Test Server of Yves](https://uk-g8-1.demo.greenitglobe.com/CBGrid/Virtual%20Machine?id=1405) we always monitored the progress in a separate session on the master node using the `tailf` command:

```
cd opt/code/{arbriatray-name}
tailf G8_testing/functional_testing/Openvcloud/logs/openvcloud_testsuite.log
```

At the end of the test both `testresults.xml` and `logs/openvcloud_testsuite.log` were copied into `/opt/testresults`, where a subdirectories exists for each test:

```
|-- ACL
|   |-- a_basic_operations
|   |   |-- acl_account_test
|   |   |-- acl_cloudspace_test
|   |   `-- acl_machine_test
|   `-- b_try_operations
|       |-- acl_account_test
|       |-- acl_cloudspace_test
|       `-- acl_machine_test
`-- OVC
    |-- a_basic
    |   |-- machine_tests
    |   `-- network_tests
    `-- b_extended
        |-- account_cloudspace_tests
        |-- cloudspace_tests
        |-- jumpscale_tests
        `-- machine_tests
```        

We used `xmllint` the quickly review `testresults.xml`:

```
xmllint --format testresults.xml
```

Installed like this:

```
sudo apt-get install libxml2-utils
```


There are basically two test suites for OpenvCloud:

- [API Test Suite](#api)
- [Portals Test Suite](#portals)

Here below

<a id="api"></a>
### API Test Suites

- [ACL API Test Suite](#acl-apis)
  - [Basic tests](#acl-basic)
    - [Accounts](#account-basic)
    - [Cloud Spaces](#cloudspace-basic)
    - [Virtual Machines](#vm-basic)
  - [Extended tests](#acl-extended)
    - [Accounts](#account-extended)
    - [Cloud Spaces](#cloudspace-extended)
    - [Virtual Machines](#vm-extended)
- [Other APIs Test Suite](#other-apis)
  - [Basic tests](#other-basic)
  - [Extended tests](#other-extended)


<a id="acl-apis"></a>
#### ACL API Test Suite

- [Basic ACL API tests](#acl-basic)
- [Extended tests](#acl-extended)

Running all (basic + extended) ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL
```

Result: FAILED, but no count of errors and failed tests
See: /opt/testresults/ACL


<a id="acl-basic"></a>
##### Basic ACL API tests

<a id="account-basic"></a>
- Running the **Account** basic ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations/acl_account_test.py
  ```

  Result: 5 tests, 0 failures, 2 errors in 20.7s
  See: /opt/testresults/ACL/a_basic_operations/acl_account_test


<a id="cloudspace-basic"></a>
- Running the **Cloud Space** basic ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations/acl_cloudspace_test.py
  ```

  Result: 21 tests, 0 failures, 21 errors in 48.5s
  See: /opt/testresults/ACL/a_basic_operations/acl_cloudspace_test


<a id="vm-basic"></a>
- Running the **Virtual Machines** basic ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations/acl_machine_test.py
  ```

  Result: 8 tests, 0 failures, 8 errors in 17.1s
  See: /opt/testresults/ACL/a_basic_operations/acl_machine_test


<a id="acl-basic-all"></a>
- Or running **All** basic ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations
  ```

  Result: 34 tests, 0 failures, 2 errors in 2368.4s
  See: /opt/testresults/ACL/a_basic_operations


<a id="acl-extended"></a>
##### Extended ACL API tests

<a id="account-extended"></a>
- Running the **Account** extended ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations/acl_account_test.py
  ```

  Result: 129 tests, 4 failures, 3 errors in 8282.1s
  See: /opt/testresults/ACL/b_try_operations/acl_account_test


<a id="cloudspace-extended"></a>
- Running the **Cloud Space** extended ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations/acl_cloudspace_test.py
  ```

  Result: 102 tests, 0 failures, 66 errors in 2389.1s
  See: /opt/testresults/ACL/b_try_operations/acl_cloudspace_test


<a id="vm-extended"></a>
- Running the **Virtual Machines** extended ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations/acl_machine_test.py
  ```

  Result: 65 tests, 0 failures, 64 errors in 192.4s
  See: /opt/testresults/ACL/b_try_operations/acl_machine_test/


<a id="acl-extended-all"></a>
- Or running **All** extended ACL API tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations
  ```

  Result: 296 tests, 5 failures, 78 errors in 13774.9s
  See: /opt/testresults/ACL/b_try_operations


<a id="other-apis"></a>
#### Other OpenvCloud APIs, covering all non-ACL APIs

- [Other OVC API Basic Tests](#other-basic)
- [Other OVC API Extended Tests](#other-extended)

Running all (basic + extended) other API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC
```

Result: ...
See: /opt/testresults/ACL


<a id="other-basic"></a>
##### Other OVC API Basic Tests

<a id="basic-machine"></a>
- All basic **machine** tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/a_basic/machine_tests.py
  ```

  Result: 21 tests, 6 failures, 4 errors in 1854.2s
  See: /opt/testresults/OVC/a_basic/machine_tests/testresults.xml

<a id="basic-network"></a>
- All basic **network** tests

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/a_basic/network_tests.py
  ```

  Result: 4 tests, 0 failures, 1 error in 778.0s
  See: /opt/testresults/OVC/a_basic/network_tests/testresults.xml


<a id="other-extended"></a>
##### Other OVC API Extended Tests

- All extended **Account** tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/b_extended/account_cloudspace_tests.py
  ```

  Result: 3 tests, 1 failure, 2 errors in 7.8s
  See: /opt/testresults//OVC/b_extended/account_cloudspace_tests/testresults.xml


- All extended **Cloud Space** tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/b_extended/cloudspace_tests.py
  ```

  Result: 1 test, 0 failures, 1 error in 2.5s
  See: /opt/testresults/OVC/b_extended/cloudspace_tests/testresults.xml


- All extended **JumpScale** tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/b_extended/jumpscale_tests.py
  ```

  Result: OK!  1 test, 0 failures, 0 errors in 0.0s
  See: /opt/testresults/OVC/b_extended/jumpscale_tests/testresults.xml


- All extended **Machine** tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/b_extended/machine_tests.py
  ```

  Result: 5 tests, 0 failures, 5 errors in 11.1s
  See: /opt/testresults/OVC/b_extended/machine_tests/testresults.xml


- All other OVC API extended tests:

  ```
  bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/OVC/b_extended
  ```

  Result: 10 tests, 1 failure, 7 errors in 95.8s
  See: /opt/testresults/OVC/b_extended


<a id="portals"></a>
### Portals Test Suite

- [End User Portal tests](#end-user)
- [Admin Portal tests](#admin-portal)

For this tests we had to clone the `selenium-hub-compatable` branch:

```
tmux a -t selenium
cd /opt/code/github/selenium
git clone -b selenium-hub-compatable git@github.com:0-complexity/G8_testing.git
cd G8_client
```

<a id="end-user"></a>
#### End User Portal tests

- Running all End User Portal tests:

  ```
  sudo bash functional_testing/Openvcloud/ovc_master_hosted/Portal/run_portal_tests.sh -u chrome -i {username} -p {password} -s {secret} -d testcases/end_user http://ma-g8-1.demo.greenitglobe.com ma-g8-1
  ```


<a id="admin-portal"></a>
#### Admin Portal tests

- Running all Admin Portal tests:

  ```
  sudo bash functional_testing/Openvcloud/ovc_master_hosted/Portal/run_portal_tests.sh -u chrome -i {username} -p {password} -s {secret} -d testcases/admin_portal http://ma-g8-1.demo.greenitglobe.com ma-g8-1
  ```

  Result: [All Cloud Broker Portal tests fail with AngularNotFoundException error](https://github.com/0-complexity/G8_testing/issues/87)

  Probably something wrong with the test script, since there clearly nothing wrong with the Cloud Broker Portal.
