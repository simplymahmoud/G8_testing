.. _OVC:

API Test Suites
-------------------------


ACL API Test Suite
******************

Basic Tests
===============
Used to test the basic (the happy path scenarios) access control on three levels account, cloud_space and virtual_machine.

Basic Accounts Tests
^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_account_test

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_account_test.Read
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_account_test.Write
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_account_test.Admin
    :members:
    :undoc-members:
    :show-inheritance:

Basic Cloud Spaces Tests
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_cloudspace_test

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_cloudspace_test.Read
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_cloudspace_test.Write
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_cloudspace_test.Admin
    :members:
    :undoc-members:
    :show-inheritance:

Basic Virtual Machines Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_machine_test

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_machine_test.Read
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_machine_test.Write
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_machine_test.Admin
    :members:
    :undoc-members:
    :show-inheritance:

Extended Tests
==================

Used to test the not-acceptable access control (the un-happy path scenarios) on three levels account, cloud_space and virtual_machine.

Extended Accounts Tests
^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_account_test

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_account_test.Read
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_account_test.Write
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_account_test.Admin
    :members:
    :undoc-members:
    :show-inheritance:

Extended Cloud Spaces Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_cloudspace_test

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_cloudspace_test.Read
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_cloudspace_test.Write
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_cloudspace_test.Admin
    :members:
    :undoc-members:
    :show-inheritance:

Extended Virtual Machines Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_machine_test

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_machine_test.Read
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_machine_test.Write
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.ACL.b_try_operations.acl_machine_test.Admin
    :members:
    :undoc-members:
    :show-inheritance:


Other API Test Suite
********************
Used to test the basic cloud_api for the openvcloud component

Basic Tests
===========

Basic Machines Tests
^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.OVC.a_basic.machine_tests
.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.OVC.a_basic.machine_tests.BasicTests
    :members:
    :undoc-members:
    :show-inheritance:

Basic Network Tests
^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.OVC.a_basic.network_tests
.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.OVC.a_basic.network_tests.NetworkBasicTests
    :members:
    :undoc-members:
    :show-inheritance:


Extended Tests
==============

Extended Cloud Space Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.account_cloudspace_tests
.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.account_cloudspace_tests.ExtendedTests
    :members:
    :undoc-members:
    :show-inheritance:


.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.cloudspace_tests
.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.cloudspace_tests.CloudspaceTests
    :members:
    :undoc-members:
    :show-inheritance:


Extended JumpScale Tests
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.jumpscale_tests
.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.jumpscale_tests.JumpscaleTests
    :members:
    :undoc-members:
    :show-inheritance:

Extended Machine Tests
^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.machine_tests
.. autoclass:: functional_testing.Openvcloud.ovc_master_hosted.OVC.b_extended.machine_tests.ExtendedTests
    :members:
    :undoc-members:
    :show-inheritance:

