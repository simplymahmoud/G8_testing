from JumpScale import j
from JumpScale.baselib.http_client.HttpClient import HTTPError
import logging
import unittest
import uuid
import time
import netaddr
import signal
from nose.tools import TimeExpired
from testconfig import config
SESSION_DATA = {'vms': []}


class API(object):
    API = {}

    def __init__(self):
        self._models = None
        self._portalclient = None
        self._cloudapi = None
        self._cloudbroker = None

    def __getattr__(self, item):
        def set_api(attr):
            API.API[item] = attr
            setattr(self, item, attr)
            return attr

        if item in API.API:
            attr = API.API[item]
            setattr(self, item, attr)
            return attr
        else:
            if item == 'models':
                return set_api(j.clients.osis.getNamespace('cloudbroker'))
            elif item == 'portalclient':
                return set_api(j.clients.portal.getByInstance('main'))
            else:
                actor = getattr(self.portalclient.actors, item)
                return set_api(actor)
        raise AttributeError(item)


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.api = API()
        super(BaseTest, self).__init__(*args, **kwargs)

    def setUp(self):

        self.CLEANUP = {'username': [], 'accountId': [],'groupname':[]}
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('openvcloud_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

        def timeout_handler(signum, frame):
            raise TimeExpired('Timeout expired before end of test %s' % self._testID)

        # adding a signal alarm for timing out the test if it took longer than 15 minutes
        signal.signal(signal.SIGALRM, timeout_handler)
        if 'OVC-003' in self._testID:
            signal.alarm(2 * 900)
        else:
            signal.alarm(900)

    def default_setup(self,create_default_cloudspace = True):
        self.create_default_cloudspace= create_default_cloudspace 
        self.location = self.get_location()['locationCode']    
        self.account_owner = self.username
        self.lg('- create account for :%s' % self.account_owner)
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner,
                                                          self.email)

        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)
   
	if self.create_default_cloudspace:
		self.lg('- create default cloudspace for :%s' % self.account_owner)
		self.cloudspace_id = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                             location=self.location,
                                                             access=self.account_owner,
                                                             api=self.account_owner_api,
                                                             name='default')

    def acl_setup(self, create_default_cloudspace=True):
        self.default_setup(create_default_cloudspace)
        self.user = self.cloudbroker_user_create()
        self.user_api = self.get_authenticated_user_api(self.user)

    def cloudapi_cloudspace_create(self, account_id, location, access, api=None,
                                   name='', maxMemoryCapacity=-1, maxDiskCapacity=-1,
                                   maxCPUCapacity=-1, maxNumPublicIP=-1):
        if api is None:
            api = self.api
        cloudspaceId = api.cloudapi.cloudspaces.create(
            accountId=account_id, location=location, access=access,
            name=name or str(uuid.uuid4()).replace('-', '')[0:10],
            maxMemoryCapacity=maxMemoryCapacity, maxVDiskCapacity=maxDiskCapacity,
            maxCPUCapacity=maxCPUCapacity, maxNumPublicIP=maxNumPublicIP)
        self.assertTrue(cloudspaceId)
        self.wait_for_status('DEPLOYED', api.cloudapi.cloudspaces.get,
                             cloudspaceId=cloudspaceId)
        return cloudspaceId

    def cloudbroker_cloudspace_create(self, account_id, location, access, api=None,
                                   name='', maxMemoryCapacity=-1, maxDiskCapacity=-1,
                                   maxCPUCapacity=-1, maxNumPublicIP=-1):
        if api is None:
            api = self.api
        cloudspaceId = api.cloudbroker.cloudspace.create(
            accountId=account_id, location=location, access=access,
            name=name or str(uuid.uuid4()).replace('-', '')[0:10],
            maxMemoryCapacity=maxMemoryCapacity, maxVDiskCapacity=maxDiskCapacity,
            maxCPUCapacity=maxCPUCapacity, maxNumPublicIP=maxNumPublicIP)
        self.assertTrue(cloudspaceId)
        self.wait_for_status('DEPLOYED', api.cloudapi.cloudspaces.get,
                             cloudspaceId=cloudspaceId)
        return cloudspaceId

    def cloudbroker_account_create(self, name, username, email, maxMemoryCapacity=-1,
                                   maxVDiskCapacity=-1, maxCPUCapacity=-1, maxNumPublicIP=-1):
        accountId = self.api.cloudbroker.account.create(name, username, email,
                                                        maxMemoryCapacity=maxMemoryCapacity,
                                                        maxVDiskCapacity=maxVDiskCapacity,
                                                        maxCPUCapacity=maxCPUCapacity,
                                                        maxNumPublicIP=maxNumPublicIP)
        self.assertTrue(accountId, 'Failed to create account for user %s!' % username)
        self.CLEANUP['accountId'].append(accountId)
        self.lg('- account ID: %s' % accountId)
        return accountId

    def cloudbroker_user_create(self, username='', email='', password='',group=[],api=None):
        if api is None:
            api = self.api
        username = username or str(uuid.uuid4()).replace('-', '')[0:10]

        api.cloudbroker.user.create(username=username, emailaddress=email or "%s@example.com" % username,
                                         password=password or username,groups=group)
        self.CLEANUP['username'].append(username)
        return username

    def get_authenticated_user_api(self, username, password=''):
        """
        Create authenticated cloud APIs for a specific user

        :returns user_api: cloud_api authenticated with the user name and password
        """
        user_api = j.clients.portal.get2()
        user_api.system.usermanager.authenticate(name=username, secret=password or username)
        return user_api

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))

    def lg(self, msg):
        self._logger.info(msg)

    def get_cloudspace(self):
        if 'cloudspaceid' not in SESSION_DATA:
            cloudspaces = self.api.cloudapi.cloudspaces.list()
            self.assertIsInstance(cloudspaces, list)
            self.assertTrue(cloudspaces)
            SESSION_DATA['cloudspaceid'] = cloudspaces[0]['id']
        return SESSION_DATA['cloudspaceid']

    def get_location(self):
        env_location = config['main']['environment']
        self.assertTrue(env_location)
        locations = self.api.cloudapi.locations.list()
        self.assertTrue(locations)
        for location in locations:
            if env_location == location['locationCode']:
                return location
        else:
            raise Exception("can't find the %s environment location in grid" % env_location)

    def stop_vm(self, vmid):
        self.api.cloudapi.machines.stop(vmid)
        try:
            self.waitForStatus(vmid, 'HALTED', timeout=10)
        except AssertionError:
            self.api.cloudapi.machines.stop(vmid)
            self.waitForStatus(vmid, 'HALTED')

    def get_image(self):
        images = self.api.cloudapi.images.list()
        self.assertTrue(images)
        return images[0]

    def get_size(self, cloudspace_id):
        sizes = self.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id)
        self.assertTrue(sizes)
        return sizes[0]

    def cloudapi_create_machine(self, cloudspace_id, api='', name='', size_id=0, image_id=0,
                                disksize=10, datadisks=[], wait=True, stackId=None):
        api = api or self.api
        name = name or str(uuid.uuid4())
        sizeId = size_id or self.get_size(cloudspace_id)['id']
        imageId = image_id or self.get_image()['id']

        if not stackId:
            machine_id = api.cloudapi.machines.create(cloudspaceId=cloudspace_id, name=name,
                                                      sizeId=sizeId, imageId=imageId,
                                                      disksize=disksize, datadisks=datadisks)
        else:
            machine_id = api.cloudbroker.machine.createOnStack(cloudspaceId=cloudspace_id, name=name,
                                                               sizeId=sizeId, imageId=imageId,
                                                               disksize=disksize, stackid=stackId)
        self.assertTrue(machine_id)
        if wait:
            self.wait_for_status('DEPLOYED', api.cloudapi.cloudspaces.get,
                                 cloudspaceId=cloudspace_id)
        machine = api.cloudapi.machines.get(machineId=machine_id)
        self.assertEqual(machine['status'], 'RUNNING')
        return machine_id
    def cloudbroker_create_machine(self, cloudspace_id, api='', name='', size_id=0, image_id=0,
                                disksize=10, datadisks=[], wait=True, stackId=None):
        api = api or self.api
        name = name or str(uuid.uuid4())
        sizeId = size_id or self.get_size(cloudspace_id)['id']
        imageId = image_id or self.get_image()['id']

        if not stackId:
            machine_id = api.cloudbroker.machine.create(cloudspaceId=cloudspace_id, name=name,
                                                      sizeId=sizeId, imageId=imageId,
                                                      disksize=disksize, datadisks=datadisks)
        else:
            machine_id = api.cloudbroker.machine.createOnStack(cloudspaceId=cloudspace_id, name=name,
                                                               sizeId=sizeId, imageId=imageId,
                                                               disksize=disksize, stackid=stackId)
        self.assertTrue(machine_id)
        if wait:
            self.wait_for_status('DEPLOYED', api.cloudapi.cloudspaces.get,
                                 cloudspaceId=cloudspace_id)
        machine = api.cloudapi.machines.get(machineId=machine_id)
        self.assertEqual(machine['status'], 'RUNNING')
        return machine_id

    def cloudbroker_group_create(self, name,group_domain ,description ):

        group_status = self.api.system.usermanager.createGroup(name=name,domain=group_domain,description=description)
        self.lg('groupstatues %s ' % group_status)
        self.assertTrue(group_status)
        self.CLEANUP['groupname'] = [name]

    def cloudbroker_group_edit(self,groupname,groupdomain,description,users):

        edit_succeed=self.api.system.usermanager.editGroup(name= groupname,domain= groupdomain,description="test",users=users)
        return edit_succeed

    def get_user_group_list(self,username):
        user_group_list=self.api.system.usermanager.usergroupsget(user=username)
        self.lg('get groups for user %s' % username)



        user_group_list=self.api.system.usermanager.usergroupsget(user=username)
        return user_group_list

    def wait_for_status(self, status, func, timeout=300, **kwargs):
        """
        A generic utility method that gets a resource and wait for resource status

        :param status: the status to wait for
        :param func: the function used to get the resource
        :param kwargs: the parameters to be sent to func to get resource
        """
        resource = func(**kwargs)  # get resource
        self.assertTrue(resource)
        for _ in xrange(timeout):
            if resource['status'] == status:
                break
            time.sleep(1)
            resource = func(**kwargs)  # get resource
        self.assertEqual(resource['status'], status)

    def add_user_to_account(self, account_id, user, accesstype, api=''):
        api = api or self.api
        api.cloudapi.accounts.addUser(accountId=account_id,
                                      userId=user,
                                      accesstype=accesstype)

        account = self.api.cloudapi.accounts.get(accountId=account_id)
        self.assertIn(user, [acl['userGroupId'] for acl in account['acl']])
        acl_user = [acl for acl in account['acl'] if acl['userGroupId'] == user][0]
        self.assertEqual(acl_user['right'], accesstype)

    def add_user_to_cloudspace(self, cloudspace_id, user, accesstype, api=''):
        api = api or self.api
        api.cloudapi.cloudspaces.addUser(cloudspaceId=cloudspace_id,
                                         userId=user,
                                         accesstype=accesstype)

        cloudspace = self.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        self.assertIn(user, [acl['userGroupId'] for acl in cloudspace['acl']])
        acl_user = [acl for acl in cloudspace['acl'] if acl['userGroupId'] == user][0]
        self.assertEqual(acl_user['right'], accesstype)

    def add_user_to_machine(self, machine_id, user, accesstype, api=''):
        api = api or self.api
        api.cloudapi.machines.addUser(machineId=machine_id,
                                      userId=user,
                                      accesstype=accesstype)

        machine = self.api.cloudapi.machines.get(machineId=machine_id)
        self.assertIn(user, [acl['userGroupId'] for acl in machine['acl']])
        acl_user = [acl for acl in machine['acl'] if acl['userGroupId'] == user][0]
        self.assertEqual(acl_user['right'], accesstype)

    def _machine_list_scenario_base(self):
        self.lg('1- Create 1 machine for account owner')
        machine_id = self.cloudapi_create_machine(self.cloudspace_id,
                                                  self.account_owner_api)
        self.lg('2- Give the user read access to the newly created machine')
        self.account_owner_api.cloudapi.machines.addUser(
            machineId=machine_id, userId=self.user, accesstype='R')

        self.lg('3- Try list user\'s machines, should return list with 1 machine')
        machines = self.user_api.cloudapi.machines.list(cloudspaceId=self.cloudspace_id)
        self.assertEqual(len(machines), 1, 'Failed to list all account owner machines!')

    def _machine_addUser_scenario_base(self):
        self.lg('1- Creating machine to the account_owner\' default cloud space')
        machine_id = self.cloudapi_create_machine(self.cloudspace_id,
                                                  self.account_owner_api)

        self.lg('2- Give the user write access to the cloud space')
        self.account_owner_api.cloudapi.cloudspaces.addUser(cloudspaceId=self.cloudspace_id,
                                                            userId=self.user, accesstype='CRX')
        self.lg('3- Creating user2')
        self.user2 = self.cloudbroker_user_create()
        self.user2_api = self.get_authenticated_user_api(self.user2)

        self.lg('4- The user gives user2 write access to the newly created machine')
        self.user_api.cloudapi.machines.addUser(machineId=machine_id,
                                                userId=self.user2, accesstype='CRX')
        machine = self.api.cloudapi.machines.get(machine_id)
        return machine

    def add_portforwarding(self, machine_id, api='', cloudspace_id='', cs_publicip='', cs_publicport=444, vm_port=22,
                           protocol='tcp'):
        api = api or self.api
        # wait until machine takes an ip
        time.sleep(60)

        cloudspace_id = cloudspace_id or self.cloudspace_id
        cloudspace = self.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        cs_publicip = cs_publicip or str(netaddr.IPNetwork(cloudspace['publicipaddress']).ip)
        api.cloudapi.portforwarding.create(cloudspaceId=cloudspace_id,
                                           publicIp=cs_publicip,
                                           publicPort=cs_publicport,
                                           machineId=machine_id,
                                           localPort=vm_port,
                                           protocol=protocol)
        return cs_publicip


    def cloudbroker_add_portforwarding(self, machine_id, api='', cloudspace_id='', cs_publicip='', cs_publicport=444, vm_port=22,
                           protocol='tcp'):
        api = api or self.api
        # wait until machine takes an ip
        time.sleep(60)

        cloudspace_id = cloudspace_id or self.cloudspace_id
        cloudspace = self.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        cs_publicip = cs_publicip or str(netaddr.IPNetwork(cloudspace['publicipaddress']).ip)
        api.cloudbrocker.machine.createPortForward(destPort=cs_publicport,machineId=machine_id,localPort=vm_port,proto=protocol)

        return cs_publicip

    def get_cloudspace_network_id(self, cloudspaceID):
        # This function take the cloudspace ID and return its network ID
        return self.api.models.cloudspace.get(cloudspaceID).networkId

    def get_node_gid(self, stackId):
        ccl = j.clients.osis.getNamespace('cloudbroker')
        scl = j.clients.osis.getNamespace('system')
        nodeId = ccl.stack.get(stackId).referenceId
        return scl.node.get(int(nodeId)).gid

    def get_running_stackId(self):
        ccl = j.clients.osis.getNamespace('cloudbroker')
        scl = j.clients.osis.getNamespace('system')
        stacks_list = ccl.stack.list()
        for stackId in stacks_list:
            nodeId = ccl.stack.get(stackId).referenceId
            node = scl.node.get(int(nodeId))
            if node.active == True:
                return stackId
        return -1

    def get_physical_node_id(self, cloudspaceID):
        # This function take the cloudspace ID and return its physical node ID
        netID = self.get_cloudspace_network_id(cloudspaceID)
        vcl = j.clients.osis.getNamespace('vfw')
        return vcl.virtualfirewall.get('%s_%s' % (j.application.whoAmI.gid, str(netID))).nid

    def get_machine_nodeID(self, machineId):
        ccl = j.clients.osis.getNamespace('cloudbroker')
        machine = ccl.vmachine.get(machineId)
        stackID = machine.stackId
        nodeID = ccl.stack.get(stackID).referenceId
        return nodeID

    def get_nodeId_to_move_VFW_to(self, current_VFW_nodeId):
        scl = j.clients.osis.getNamespace('system')
        nodeIds_list = scl.node.list({})
        nodeIds_list.remove(scl.node.get('%s_%s' % (j.application.whoAmI.gid, str(current_VFW_nodeId))).guid)
        for nodeId in nodeIds_list[1:]:
            node = scl.node.get(nodeId)
            node_details=self.api.system.gridmanager.getNodes(id = node.id)
            if (node.active == True ) and ( "fw" in node_details[0]["roles"]): 
                return node.id
        return -1

    def execute_command_on_physical_node(self, command, nodeid):
        # This function execute a command on a physical real node
        acl = j.clients.agentcontroller.get()
        output = acl.executeJumpscript('jumpscale', 'exec', nid=nodeid, args={'cmd': command})
        if output['state'] == 'OK':
            if 'ERROR' not in output['result'][1]:
                return output['result'][1]
            else:
                raise NameError("This command:" + command + "is wrong")
        else:
            raise NameError("Node result state is not OK")


class BasicACLTest(BaseTest):
    def setUp(self):
        """
        Setup environment for the test case.
        """
        super(BasicACLTest, self).setUp()

        self.username = str(uuid.uuid4()).replace('-', '')[0:10] + self.shortDescription().split(' ')[
            0].lower().replace('-', '')
        self.lg(' ***************************** ')
        self.lg('setUp -- create user %s' % self.username)
        password = self.username
        self.email = "%s@example.com" % str(uuid.uuid4())
        self.CLEANUP['username'] = [self.username]
        self.api.cloudbroker.user.create(self.username, self.email, password)

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        api = API()
        accountIds = self.CLEANUP.get('accountId')
        if accountIds:
            for account in accountIds:
                self.lg('Teardown -- delete account: %s' % account)
                try:
                    api.cloudbroker.account.delete(accountId=account, reason="Teardown delete")
                    self.wait_for_status('DESTROYED', self.api.cloudapi.accounts.get,
                                         accountId=self.account_id)
                except HTTPError as e:
                    # Account is already deleted
                    self.assertEqual(e.status_code, 404)
        users = self.CLEANUP.get('username')
        if users:
            for user in users:
                self.lg('Teardown -- delete user: %s' % user)
                api.cloudbroker.user.delete(user)
        groups = self.CLEANUP.get('groupname')
        if groups:
            print groups
            for group in groups:
                self.lg('Teardown -- delete group: %s' % group)
                self.api.system.usermanager.deleteGroup(id=group)
        super(BasicACLTest, self).tearDown()
