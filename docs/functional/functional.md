## Functional Testing

This section describes the tests to be executed in order to validate the basic functionality of a G8 installation.

Functional testing requires that the system was installed properly, as documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), more specifically in the section [Installation of an OpenvCloud Environment](https://gig.gitbooks.io/ovcdoc_public/content/Installation/Installation.html).

Following functional tests are available:

- [Portal Test Suite](#portal)
  - [End User Portal tests](#end-user)
    - [Home page](#home-page)
    - [Machine page](#home-page)
    - [Cloud APIs page](#api-page)
  - [Admin Portal tests](#admin-portal)
    - [Home page](#admin-home)
    - [Cloud Broker Portal](#cloud-broker)
    - [Grid Portal](#grid-portal)

- [API Test Suite](#api)
  - [Access Control List (ACL) APIs](#acl-apis)
    - [Basic tests](#acl-basic)
      - [Accounts](#account-basic)
      - [Cloud Spaces](#cloudspace-basic)
      - [Virtual Machines](#vm-basic)
    - [Extended tests](#acl-extended)
      - [Accounts](#account-extended)
      - [Cloud Spaces](#cloudspace-extended)
      - [Virtual Machines](#vm-extended)
  - [Other OpenvCloud APIs, covering all non-ACL APIs](#other-apis)
    - [Basic Tests](#other-basic)
      - [Basic Machine tests](#basic-machine)
      - [Basic Network tests](#basic-network)
    - [Extended Tests](#other-extended)
      - [Extended Account tests](#account-tests)
      - [Extended Cloud Space tests](#cloudspace-tests)
      - [Extended JumpScale tests](#jumpscale-tests)
      - [Extended machine tests](#machine-tests)

- [Network configuration test](#network-config)
- [Virtual machines limit test](#vm-limit)
- [Cloud spaces limit test](#cloudspace-limit)
- [VM live migration test](#vm-migration)
- [Node maintenance test](#node-maintenance)
- [Snapshots limit test](#snapshots-limit)


The functional tests can be categorized into three categories:

- [Hosted on the master node](openvcloud/ovc_master_hosted/ovc_master_hosted.md)
- [Hosted on any compute node](openvcloud/compute_node_hosted/compute_node_hosted.md)
- [Hosted on any remote machine](openvcloud/remote_machine_hosted/remote_machine_hosted.md)

Only the Portal and API tests can run from both the master node or any remote node, that's why they appear under both categories:

| Section                                        | master node | compute node | remote node |
|:-----------------------------------------------|:-----------:|:------------:|:-----------:|
|[Portal testing](#portal)                       | X           |              | X           |
|[API testing](#api)                             | X           |              | X           |
|[Network configuration test](#network-config)   |             | X            |             |
|[Virtual machines limit test](#vm-limit)        |             | X            |             |
|[Cloud spaces limit test](#cloudspace-limit)    |             | X            |             |
|[VM live migration test](#vm-migration)         |             | X            |             |
|[Node maintenance test](#node-maintenance)      |             | X            |             |
|[Snapshots limit test](#snapshots-limit)        |             | X            |             |


<a id="portal"></a>
### Portal tests

- [End User Portal tests](#end-user)
- [Admin Portal tests](#admin-portal)

See [Portal Testing](openvcloud/remote_machine_hosted//portal/portal.md) for instructions on how to run the Portal tests.

<a id="end-user"></a>
#### End User Portal tests

- [Home page](#home-page)
- [Machine page](#home-page)
- [Cloud APIs page](#api-page) (not implemented yet)

<a id="home-page"></a>
##### Home page

- LoginLogoutPortalTests class (`test01_login_logout.py`)
  - test001_login_and_portal_title()
  - test002_logout_and_portal_title()
  - test003_login_wrong_username()
  - test004_login_wrong_password()
  - test005_login_wrong_username_password()
- QuickTutorialGuide class (`test02_getting_started.py`)
  - test01_intro()
  - test02_cloudspace()
  - test03_machines()
  - test04_defense_shield()
- KnowledgeBase class (`test03_knowlege_base.py`)
  - test01_technical_tutorials()
  - test02_technical_tutorials_first_tab()
  - test03_technical_tutorials_second_tab()
  - test04_technical_tutorials_third_tab()
  - test05_technical_tutorials_forth_tab()
  - test06_technical_tutorials_fifth_tab()
  - test07_technical_tutorials_sixth_tab()
  - test08_technical_tutorials_seventh_tab()
- Support class (`test04_support.py`)
  - test01_support()
- ChangePassword class (`test05_verify_change_user_password.py`)
  - test01_verify_change_user_password()


<a id="machine-page"></a>
##### Machine page

- Write class (`test01_machine_operations.py`)
  - test01_machine_stop_start_reboot_reset_pause_resume()
  - test02_machine_create_rollback_delete_snapshot()
- Read class (`test02_machine_creation.py`)
  - test06_machine_create()
- DefenseShield class (`test03_defense_shield.py`)
  - test001_defense_shield_page()

<a id="api-page"></a>
##### Cloud APIs page

Not implemented yet:

- CloudSpaces class (`test01_cloudapi__cloudspaces.py`)
- Machines class (`test02_ cloudapi__machines.py`)
- Accounts class (`test02_ cloudapi__machines.py`)
- PortForwarding class (`test04_ cloudapi__portforwarding.py`)
- Locations class (`test05_cloudapi__locations.py`)
- Users class (`test06_cloudapi__users.py`)
- Disks class (`test07_cloudapi__disks.py`)
- Sizes class (`test08_cloudapi__sizes.py`)
- Images class (`test09_cloudapi__images.py`)


<a id="admin-portal"></a>
#### Admin Portal tests

- [Home](#admin-home)
- [Cloud Broker Portal](#cloud-broker)
- [Grid Portal](#grid-portal)


<a id="admin-home"></a>
##### Admin Home page

- `Account` class (`test01_create_account_user_cs_vm.py`)
  - `test01_create_account_user_cs_vm()``
- `AdminMenu` class (`test02_admin_menu.py`)
  - `test01_admin_menu_items()``


<a id="cloud-broker"></a>
##### Cloud Broker Portal

  - **Accounts** page tests, implemented in the `AccountsTests` class (`test01_accounts.py`):
    - `test01_edit_account()`
    - `test02_disable_enable_account()`
    - `test03_add_account_with_decimal_limitations()`
    - `test04_account_page_paging_table()`
    - `test05_account_page_table_paging_buttons()`
    - `test06_account_page_table_sorting()`
  - **Cloud Spaces** page tests, implemented in the `CloudspacesTests` class (`test02_cloudspaces.py`):
    - `test01_cloudspace_page_paging_table()``
    - `test05_cloudspace_page_table_paging_buttons()``
    - `test06_cloudspace_page_table_sorting()``
  - **Users** page tests, implemented in the `UsersTests` class (`test03_users.py`)
    - `test01_users_page_paging_table()`
    - `test02_users_page_table_paging_buttons()`
    - `test03_users_page_table_sorting()`
  - **Virtual Machines** page tests, implemented in the `VirtualMachinesTest` class (`test04_virtualmachines.py`)
   - `test01_vm_page_paging_table()`
   - `test02_vms_page_table_paging_buttons()`
   - `test03_vms_page_table_sorting()`


<a id="grid-portal"></a>
##### Grid Portal

- **Grids Nodes** page tests, implemented in the `GridTests` class (`test01_error_conditions.py`)
  - `test001_error_condition_page()`
- **StatusOverview** page tests, implemented in the `StatusTests` class (`test02_status_overview.py`)
  - `test01_check_process_status()`
  - `test02_health_check()`
- **Virtual Machines** page tests, implemented in the `VMachinesTests` class (`test03_vmachines.py`)
 - Not implemented yet


<a id="api"></a>
### API Test Suite

- [Access Control List (ACL) APIs](#acl-apis)
- [OpenvCloud APIs, covering all non-ACL APIs](#other-api)

See [API Testing](openvcloud/ovc_master_hosted/API/API.md) for instructions on how to run the API tests.


<a id="acl-apis"></a>
#### Access Control List (ACL) APIs

<a id="acl-basic"></a>
##### Basic ACL API Tests

<a id="account-basic"></a>
- Basic **Account** ACL API tests, all implemented in `ACL/a_basic_operations/acl_account_test.py`:
  - **Read** access rights tests, implemented in the `Read` class:
    - `test003_account_get_with_readonly_user()`
    - `test004_account_list_with_readonly_user()`
  - **Write** access rights tests, implemented in the `Write` class:
    - `test003_cloudspace_create()`
    - `test004_machine_createTemplate()`
 - **Admin** access rights tests, implemented in the `Admin` class:
   - `test003_account_add_update_delete_User()`

<a id="cloudspace-basic"></a>
- Basic **Cloud Space** ACL API tests, all implemented in `ACL/a_basic_operations/acl_cloudspace_test.py`:
  - **Read** access rights tests, implemented in the `Read` class:
    - `test003_cloudspace_get_with_readonly_user()`
    - `test006_cloudspace_list_with_another_cloudspace()`
    - `test007_cloudspace_list_deleted_cloudspace()`
    - `test008_cloudspace_disabled_deleted_account()`
    - `test009_machine_list_deleted_machine()`
    - `test010_machine_list_deleted_cloudspace()`
    - `test011_machine_list_disabled_deleted_account()`
    - `test012_portforwarding_list()`
  - **Write** access rights tests, implemented in the `Write` class:
    - `test003_cloudspace_deploy_getDefenseShield()`
    - `test004_cloudspace_portforwarding_add_update_delete()`
    - `test005_cloudspace_create_clone_delete_machine()`
    - `test023_machine_addUser()`
    - `test024_machine_addUser_wrong()`
    - `test025_machine_deleteUser()`
    - `test026_machine_deleteUser_wrong()`
    - `test027_machine_updateUser()`
    - `test028_machine_updateUser_wrong()`
    - `test007_resize_machine()`
  - **Admin** access rights tests, implemented in the `Admin` class:
    - `test003_cloudspace_add_update_delete_User()`
    - `test004_cloudspace_add_update_delete_User_wrong()`
    - `test005_cloudspace_update_delete()`

<a id="vm-basic"></a>
- Basic **Virtual Machine** ACL API tests, all implemented in `ACL/a_basic_operations/acl_machine_test.py`:
  - **Read** access rights tests, implemented in the `Read` class:
    - `test003_machine_get_list()`
    - `test004_machine_getConsoleUrl_listSnapshots_getHistory()`
  - **Write** access rights tests, implemented in the `Write` class:
    - `test003_machine_start_stop_reboot_reset()`
    - `test004_machine_pause_resume()`
    - `test005_machine_snapshot_create_rollback_delete()`
    - `test006_machine_update()`
  - **Admin** access rights tests, implemented in the `Admin` class:
    - `test003_machine_add_update_delete_User()`
    - `test004_machine_add_update_delete_User_wrong()`


<a id="acl-extended"></a>
##### Extended ACL API Tests

<a id="account-extended"></a>
- Extended **Account** ACL API tests, all implemented in `ACL/b_try_operations/acl_account_test.py`

<a id="cloudspace-extended"></a>
- Extended **Cloud Space** ACL API tests, all implemented in `ACL/b_try_operations/acl_cloudspace_test.py`

<a id="vm-extended"></a>
- Extended **Virtual Machine** ACL API tests, all implemented in `ACL/b_try_operations/acl_machine_test.py`


<a id="other-apis"></a>
#### Other OpenvCloud APIs, covering all non-ACL APIs

- [Other OVC API Basic Tests](#other-basic)
- [Other OVC API Extended Tests](#other-extended)

<a id="other-basic"></a>
#### Other OVC API Basic Tests

<a id="basic-machine"></a>
- All **basic machine tests** are implemented in the `BasicTests` class (`OVC/a_basic/machine_tests.py`):
    - `test001_reboot_vm()`
    - `test002_create_vmachine_withbig_disk()`
    - `test003_create_machine_with_resize()`
    - `test004_create_machine_with_resize_in_halted()`
    - `test005_add_disks_to_vmachine()`
    - `test006_machine_snapshots()`
    - `test007_cleanup_vxlans_for_stopped_deleted_vms()`
    - `test008_test_different_Language()`
    - `test009_access_docker_on_vm()`
    - `test010_enable_disable_fireWall()`
    - `test011_windowsVM_with_different_sizes()`


<a id="basic-network"></a>
- All **basic network tests** are implemented in the `NetworkBasicTests` class (`OVC/a_basic/network_tests.py`):
  - `test001_release_networkId()`
  - `test002_clean_ovs_bridge()`
  - `test003_port_forwarding_creation()`
  - `test004_move_virtual_firewall()`


<a id="other-extended"></a>
#### Other OVC API Extended Tests

<a id="account-tests"></a>
- All **extended Account tests** are implemented in the `ExtendedTests` class (`OVC/b_extended/account_cloudspace_tests.py`)

<a id="cloudspace-tests"></a>
- All **extended Cloud Space tests** are implemented in the `CloudspaceTests` class (`OVC/b_extended/cloudspace_tests.py`)

<a id="jumpscale-tests"></a>
- All **extended JumpScale tests** are implemented in the `JumpscaleTests` class (`OVC/b_extended/b_extended/jumpscale_tests.py`)

<a id="machine-tests"></a>
- All **extended machine tests** are implemented in the `ExtendedTests` class (`OVC/b_extended/machine_tests.py`)


<a id="network-config"></a>
### Network configuration test

See [Network Configuration Test](openvcloud/compute_node_hosted/1_network_config_test/1_network_config_test.md)


<a id="vm-limit"></a>
### Virtual machines limit test

See [Virtual Machines Limit Test](openvcloud/compute_node_hosted/3_Env_Limit_test/3_Env_Limit_test.md)


<a id="cloudspace-limit"></a>
### Cloud spaces limit test

See [Cloud Spaces Limit Test](/openvcloud/compute_node_hosted/5_cloudspace_limits_test/5_cloudspace_limits_test.md)


<a id="vm-migration"></a>
### VM Live migration test

See [VM Live Migration Test](openvcloud/compute_node_hosted/6_vm_live_migration_test/6_vm_live_migration_test.md)


<a id="node-maintenance"></a>
### Node maintenance test

See [Node Maintenance Test](openvcloud/compute_node_hosted/8_node_maintenance_test/8_node_maintenance_test.md)


<a id="snapshots-limit"></a>
### Snapshots limit test

See [Snapshots Limit Test](openvcloud/compute_node_hosted/9_vm_unlimited_snapshots/9_vm_unlimited snapshots.md)
