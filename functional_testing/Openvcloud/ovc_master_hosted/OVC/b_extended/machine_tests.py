# coding=utf-8
from nose_parameterized import parameterized
from ....utils.utils import BasicACLTest

from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError
import random

class ExtendedTests(BasicACLTest):

    def setUp(self):
        super(ExtendedTests, self).setUp()
        self.default_setup()

    @parameterized.expand(['Ubuntu 14.04 x64', 'Ubuntu 15.10 x64', 'Ubuntu 16.04 x64'])
    def test001_create_vmachine_with_all_disks(self, image_name):
        """ OVC-013
        *Test case for create machine with Linux image available.*

        **Test Scenario:**

        #. validate the image is exists, should succeed
        #. get all available sizes to use, should succeed
        #. create machine using given image with specific size and all available disk sizes, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- validate the image is exists, should succeed')
        images = self.api.cloudapi.images.list()
        self.assertIn(image_name,
                      [image['name'] for image in images],
                      'Image [%s] not found in the environment available images' % image_name)
        image = [image for image in images if image['name'] == image_name][0]

        self.lg('2- get all available sizes to use, should succeed')
        sizes = self.api.cloudapi.sizes.list(cloudspaceId=self.cloudspace_id)
        self.lg('- using image [%s]' % image_name)
        basic_sizes=[512,1024,4096,8192,16384,2048]
        random_sizes= random.sample(basic_sizes,3)
        for size in sizes:
            if size['memory'] not in random_sizes:
                continue
            self.lg('- using image [%s] with memory size [%s]' % (image_name, size['memory']))
            disk_sizes=[10,20,50,100,250,500,1000,2000]
            random_disks= random.sample(disk_sizes,3)

            for disk in random_disks:
                self.lg('- using image [%s] with memory size [%s] with disk '
                        '[%s]' % (image_name, size['memory'], disk))
                machine_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id,
                                                          size_id=size['id'],
                                                          image_id=image['id'],
                                                          disksize=disk)
                self.lg('- done using image [%s] with memory size [%s] with disk '
                        '[%s]' % (image_name, size['memory'], disk))
                self.lg('- delete machine to free environment resources, should succeed')
                self.api.cloudapi.machines.delete(machineId=machine_id)

        self.lg('%s ENDED' % self._testID)


    def test002_node_maintenance_stopVMs(self):
        """ OVC-019
        *Test case for putting node in maintenance with action stop all vms.*

        **Test Scenario:**

        #. create 2 VMs, should succeed
        #. put node in maintenance with action stop all vms, should succeed
        #. check that the 2 VMs have been halted
        #. enable the node back, should succeed
        #. check that the 2 VMs have returned to running status
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('1- get a running node to create VMs on')
        stackId = self.get_running_stackId()
        self.assertNotEqual(stackId, -1, msg="No active node to create VMs on")

        self.lg('2- create 2 VMs, should succeed')
        machine_Id1 = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id, stackId=stackId)
        machine_Id2 = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id, stackId=stackId)

        self.lg('3- put node in maintenance with action stop all vms, should succeed')
        gid = self.get_node_gid(stackId)
        self.api.cloudbroker.computenode.maintenance(id=stackId, gid=gid, vmaction='stop', message='testing')

        self.lg('4- check that the 2 VMs have been halted')
        self.wait_for_status('HALTED', self.api.cloudapi.machines.get, machineId=machine_Id1)
        machine_1 = self.api.cloudapi.machines.get(machineId=machine_Id1)
        self.assertEqual(machine_1['status'], 'HALTED')
        self.wait_for_status('HALTED', self.api.cloudapi.machines.get, machineId=machine_Id2)
        machine_2 = self.api.cloudapi.machines.get(machineId=machine_Id2)
        self.assertEqual(machine_2['status'], 'HALTED')

        self.lg('5- enable the node back, should succeed')
        self.api.cloudbroker.computenode.enable(id=stackId, gid=gid, message='testing')

        self.lg('6- check that the 2 VMs have returned to running status')
        self.wait_for_status('RUNNING', self.api.cloudapi.machines.get, machineId=machine_Id1)
        machine_1 = self.api.cloudapi.machines.get(machineId=machine_Id1)
        self.assertEqual(machine_1['status'], 'RUNNING')
        self.wait_for_status('RUNNING', self.api.cloudapi.machines.get, machineId=machine_Id2)
        machine_2 = self.api.cloudapi.machines.get(machineId=machine_Id2)
        self.assertEqual(machine_2['status'], 'RUNNING')

        self.lg('%s ENDED' % self._testID)

    def test003_create_vmachine_clone_with_empty_name(self):
        """ OVC-021
        *Test case for create vmachine/clone with empty name.*

        **Test Scenario:**

        #. Try to create machine with empty name, should fail
        #. Create normal machine with valid name, should succeed
        #. Stop the created machine to be able to clone it, should succeed
        #. Try to clone created machine with empty name, should fail
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- Try to create machine with empty name, should fail')
        try:
            self.api.cloudapi.machines.create(cloudspaceId=self.cloudspace_id,
                                              name='',
                                              sizeId=self.get_size(self.cloudspace_id)['id'],
                                              imageId=self.get_image()['id'],
                                              disksize=10)
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg("2- Create normal machine with valid name, should succeed")
        machine_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)
        self.machine_ids = [machine_id]

        self.lg("3- Stop the created machine to be able to clone it, should succeed")
        self.api.cloudapi.machines.stop(machineId=machine_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=machine_id)['status'], 'HALTED')

        self.lg('4- Try to clone created machine with empty name, should fail')
        try:
            self.api.cloudapi.machines.clone(machineId=machine_id, name='')
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg('%s ENDED' % self._testID)
