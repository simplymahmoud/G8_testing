# coding=utf-8
import time
import random
import unittest

from JumpScale import j
from ....utils.utils import BasicACLTest


class NetworkBasicTests(BasicACLTest):

    def setUp(self):
        super(NetworkBasicTests, self).setUp()
        self.acl_setup()

    def test001_release_networkId(self):
        """ OVC-010
        * Test case for check that deleting Account with multiple Cloud Spaces will release all Cloud Spaces network IDs*

        **Test Scenario:**

        #. create three cloudspaces with user1 and get its network ID
        #. Delete the first cloudspace
        #. Check the release network ID after destroying the first cloudspace
        #. Delete the account
        #. Check the release network ID are in the free network IDs list
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('1- create three cloudspaces with user1 and get its network ID')
        cloud_space_networkId = []
        ccl = j.clients.osis.getNamespace('cloudbroker')

        for csNumbers in range(0, 3):
            self.cloudspaceId = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                                location=self.location,
                                                                access=self.account_owner,
                                                                api=self.account_owner_api)
            cloud_space_networkId.append(ccl.cloudspace.get(self.cloudspaceId).networkId)

        self.lg('2- Delete the third cloudspace')
        self.account_owner_api.cloudapi.cloudspaces.delete(cloudspaceId=self.cloudspaceId)

        self.lg('3- Check the release network ID after destroying the third cloudspace')
        for timeDelay in range(0, 10):
            if ccl.cloudspace.get(self.cloudspaceId).networkId:
                time.sleep(1)
            else:
                break
        self.assertFalse(ccl.cloudspace.get(self.cloudspaceId).networkId)

        self.lg('4- delete account: %s' % self.account_id)
        self.api.cloudbroker.account.delete(accountId=self.account_id, reason='testing')

        self.lg('5- Check the release network ID are in the free network IDs list')
        lcl = j.clients.osis.getNamespace('libcloud')
        for csNumbers in range(0, 3):
            for timeDelay in range(0, 10):
                released_network_Id = lcl.libvirtdomain.get('networkids_%s' % j.application.whoAmI.gid)
                if str(cloud_space_networkId[csNumbers]) not in released_network_Id:
                    time.sleep(1)
                else:
                    break
            self.assertTrue(str(cloud_space_networkId[csNumbers]) in released_network_Id)
        self.lg('%s ENDED' % self._testID)

    def test002_clean_ovs_bridge(self):
        ''' OVC-011
         * Test case verify the cleaning OVS bridges when deleting a cloudspace operation

        **Test Scenario:**

        #. Create a new cloudspace and deploy it
        #. Get the cloudspace Network ID and convert it to hex
        #. Make sure that the bridge is created
        #. Delete this cloudspace
        #. make sure that the bridge is released
        '''
        self.lg('%s STARTED' % self._testID)
        self.lg('1- Create a new cloudspace and deployed it')
        cloudspace_id = self.cloudapi_cloudspace_create(self.account_id,
                                                self.location,
                                                self.account_owner)
        self.api.cloudbroker.cloudspace.deployVFW(cloudspace_id)

        self.lg('2- Get the cloudspace network ID and convert it to hex')
        self.hexNetworkID = '%04x' % self.get_cloudspace_network_id(cloudspace_id)

        self.lg('- Get the cloudspace physical node ID')
        nodID = self.get_physical_node_id(cloudspace_id)

        self.lg('3- Make sure that the bridge is created')
        command = 'ls /sys/class/net'  # All created bridges in this node
        result = self.execute_command_on_physical_node(command, nodID)
        self.assertIn('space_' + self.hexNetworkID, result)

        self.lg('4- Delete this cloudspace')
        self.account_owner_api.cloudapi.cloudspaces.delete(cloudspaceId=cloudspace_id)

        self.lg('5- Make sure that the bridge is deleted')
        result = self.execute_command_on_physical_node(command, nodID)
        self.assertNotIn('space_' + self.hexNetworkID, result)

        self.lg('%s ENDED' % self._testID)

    def test003_port_forwarding_creation(self):
        '''OVC- 007
        * Test case verify the adding port forward to a machine

        #. Create a cloudspace and get its public ip
        #. Create a virtual machine
        #. Check that the cloudspace has a public IP
        #. Create a ssh / 22 port forwarding
        #. Check the port forwarding list is updated
        #. Check connection to the VM over this port
        #. Create a ftp / 21 port forwarding
        #. Check the port forwarding list is updated
        #. Check connection to the VM over this port
        #. Create a HTTP / 80 port forwarding
        #. Check the port forwarding list is updated
        #. Check connection to the VM over this port
        #. Create HTTPS / 443 port forwarding
        #. Check the port forwarding list is updated
        #. Check connection to the VM over this port
        #. port forwarding RDP / 3389 port forwarding
        #. Check the port forwarding list is updated
        #. Check connection to the VM over this port
        '''

        self.lg('%s STARTED' % self._testID)
        self.lg('1- Create a new cloudspace')
        cloudspaceId = self.cloudapi_cloudspace_create(self.account_id,
                                                       self.location,
                                                       self.account_owner)

        self.lg('- deploy cloudspace, should succeed')
        self.api.cloudapi.cloudspaces.deploy(cloudspaceId=cloudspaceId)
        self.wait_for_status('DEPLOYED', self.api.cloudapi.cloudspaces.get,
                         cloudspaceId=cloudspaceId)

        self.lg('Check the cloudspace has a public ip')
        cloudspace_puplicIp = self.api.cloudapi.cloudspaces.get(cloudspaceId)['publicipaddress']
        self.assertNotEqual(cloudspace_puplicIp, '')

        images = self.api.cloudapi.images.list()
        for image in images:
            self.lg('- Create a new machine')
            if 'Windows' in image['name']:
                machineId = self.cloudapi_create_machine(cloudspaceId,image_id=int(image['id']),disksize=50)
            else:
                machineId = self.cloudapi_create_machine(cloudspaceId,image_id=int(image['id']))

            self.lg('- Make sure that the machine got an IP')
            machineIp = ''
            for i in range(300):
                machineIp = self.api.cloudapi.machines.get(machineId)['interfaces'][0]['ipAddress']
                if machineIp != '':
                    break
                time.sleep(1)
            self.assertNotEqual(machineIp,'')

            self.lg('Create a port forwarding which is covering all combinations')
            localPorts = [21, 22, 80, 442, 21, 3389]
            publicPort = random.randint(4000,5000)
            protocolItems = ['tcp', 'udp']
            lastAddedIndex = 0

            time.sleep(60)
            for proctocl in protocolItems:
                for localPort in localPorts:
                    self.lg("Create portforward for port %s to public port %s " % (localPort,publicPort))
                    self.api.cloudapi.portforwarding.create(cloudspaceId=cloudspaceId, publicIp=cloudspace_puplicIp,
                                                            publicPort=publicPort, machineId=machineId,
                                                            localPort=localPort, protocol=proctocl)

                    self.assertEqual(self.api.cloudapi.portforwarding.list(cloudspaceId=cloudspaceId,
                                                                           machineId=machineId)[lastAddedIndex][
                                         'localPort'],
                                     str(localPort))
                    self.assertEqual(self.api.cloudapi.portforwarding.list(cloudspaceId=cloudspaceId,
                                                                           machineId=machineId)[lastAddedIndex][
                                         'publicPort'],
                                     str(publicPort))
                    self.assertEqual(self.api.cloudapi.portforwarding.list(cloudspaceId=cloudspaceId,
                                                                           machineId=machineId)[lastAddedIndex][
                                         'protocol'],
                                     proctocl)

                    publicPort += 1
                    lastAddedIndex += 1

                    self.lg('test ssh connection')
                    if localPort == 22:
                        time.sleep(60)
                        self.lg('Get the virtual machine user name and password')
                        username = self.api.cloudapi.machines.get(machineId)['accounts'][0]['login']
                        password = self.api.cloudapi.machines.get(machineId)['accounts'][0]['password']
                        command = "sshpass -p " + password + " ssh -p " + str(publicPort) + ' ' + username + "@" + cloudspace_puplicIp + '; uname -a; '
                        acl = j.clients.agentcontroller.get()
                        output = acl.executeJumpscript('jumpscale', 'exec', nid=3 , args={'cmd': command})
                        if output['state'] == 'OK':
                           if 'Linux' not in output['result'][1]:
                                raise NameError("This command:"+command+"is wrong")
            
        self.api.cloudapi.machines.stop(machineId=machineId)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=machineId)['status'],
                         'HALTED')
        self.lg('%s ENDED' % self._testID)

    def test004_move_virtual_firewall(self):
        """ OVC-014
        * Test case for moving virtual firewall form one node to another

        **Test Scenario:**

        #. create account and cloudspace
        #. deploy the created cloudspace
        #. get nodeId of the cloudspace virtual firewall
        #. get another nodeId to move the virtual firewall to
        #. move virtual firewall to another node, should succeed

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('1- deploy the created cloudspace')
        self.api.cloudbroker.cloudspace.deployVFW(self.cloudspace_id)
        self.wait_for_status('DEPLOYED', self.account_owner_api.cloudapi.cloudspaces.get,
                             cloudspaceId=self.cloudspace_id)

        self.lg('2- get nodeId of the cloudspace virtual firewall')
        nodeId = self.get_physical_node_id(self.cloudspace_id)

        self.lg('3- get another nodeId to move the virtual firewall to')
        other_nodeId = self.get_nodeId_to_move_VFW_to(nodeId)
        self.assertNotEqual(other_nodeId, -1, msg="No active node to move the VFW to")

        self.lg('4- move virtual firewall to another node')
        self.api.cloudbroker.cloudspace.moveVirtualFirewallToFirewallNode(cloudspaceId=self.cloudspace_id,
                                                                          targetNid=other_nodeId)
        new_nodeId = self.get_physical_node_id(self.cloudspace_id)
        self.assertEqual(other_nodeId, new_nodeId)

        self.wait_for_status('DEPLOYED', self.account_owner_api.cloudapi.cloudspaces.get,
                             cloudspaceId=self.cloudspace_id)
        self.lg('%s ENDED' % self._testID)        
