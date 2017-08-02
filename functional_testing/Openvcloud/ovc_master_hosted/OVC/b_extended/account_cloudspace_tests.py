from ....utils.utils import BasicACLTest
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError


class ExtendedTests(BasicACLTest):
    def setUp(self):
        super(ExtendedTests, self).setUp()
        self.location = self.get_location()['locationCode']
        self.account_owner = self.username

    def test001_basic_resource_limits(self):

        """ OVC-016
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. create account with passing negative values in the account's limitation, should fail
        #. create account with certain limits, should succeed
        #. create cloudspace with passing negative values in the cloudspace's limitation, should fail
        #. create cloudspace that exceeds account's max_cores, should fail
        #. create cloudspace that exceeds account's max_memory, should fail
        #. create cloudspace that exceeds account's max_vdisks, should fail
        #. create cloudspace that exceeds account's max_IPs, should fail
        #. create cloudspace without exceeding account limits, should succeed
        #. Try to create another cloudspace without exceeding account limits, should fail as account\'s maxIPs=1
        #. create VM with exceeding cloudspace\'s cores number, should fail
        #. create VM with exceeding cloudspace\'s Memory, should fail
        #. create VM with exceeding cloudspace\'s disks capacity, should fail
        #. create VM with allowed limits
        #. add publicip to this VM, should fail as account's max_IPs=1
        """
        self.lg('- create account with passing negative values in the account\'s limitation')
        try:
            self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email,
                                            maxMemoryCapacity=-5, maxVDiskCapacity=-3,
                                            maxCPUCapacity=-4, maxNumPublicIP= -2)
        except HTTPError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg(' - create account with certain limits, should succeed')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner,
                                                          self.email, maxMemoryCapacity=2,
                                                          maxVDiskCapacity=60 , maxCPUCapacity=4,
                                                          maxNumPublicIP= 1)
        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

        self.lg('- create cloudspace with passing negative values in the cloudspace\'s limitation, should fail')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=-5,
                                                       maxDiskCapacity=-4, maxCPUCapacity=-3,
                                                       maxNumPublicIP=-2)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


        list =[{'mC':8, 'mM':0, 'mVD':0, 'mIP':0, 's':'max_cores'},
               {'mC':0, 'mM':8, 'mVD':0, 'mIP':0, 's':'max_memory'},
               {'mC':0, 'mM':0, 'mVD':100, 'mIP':0, 's':'max_vdisks'},
               {'mC':0, 'mM':0, 'mVD':0, 'mIP':2, 's':'max_IPs'}]
        for i in list:
            self.lg('- create cloudspace that exceeds account\'s %s, should fail'%i['s'])
            try:
                self.cloudapi_cloudspace_create(account_id=self.account_id, location=self.location,
                                                name='cs1', access=self.account_owner,
                                                api=self.account_owner_api,
                                                maxMemoryCapacity=i['mM'] or 2,
                                                maxDiskCapacity=i['mVD'] or 60,
                                                maxCPUCapacity= i['mC'] or 4,
                                                maxNumPublicIP=i['mIP'] or 1)
            except ApiError as e:
                self.lg('- expected error raised %s' % e.message)
                self.assertEqual(e.message, '400 Bad Request')


        self.lg('- create cloudspace without exceeding account limits, should succeed')
        cloudspaceId = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=2,
                                                       maxDiskCapacity=60, maxCPUCapacity=4,
                                                       maxNumPublicIP=1)

        self.lg('Try to create another cloudspace without exceeding account limits,'
                ' should fail as account\'s maxIPs=1')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs2', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=2,
                                                       maxDiskCapacity=60, maxCPUCapacity=4,
                                                       maxNumPublicIP=1)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


        self.lg('- create VM with exceeding cloudspace\'s cores number (Mem=16, C=8), '
                'should fail as (c=8)>4')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=5)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM with (Mem=8, C=4), should fail as (M=8)>2')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=4)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM with (BD=100), should fail as (BD=100)>60')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, disksize=10)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


        self.lg('- create VM with allowed limits, should succeed')
        machineId = self.cloudapi_create_machine(cloudspaceId, self.account_owner_api)

        self.lg('- Add publicip to this VM, should fail as max_IPs=1')
        try:
            self.account_owner_api.cloudapi.machines.attachExternalNetwork(machineId=machineId)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


    def test002_resource_limits_on_account_level(self):
        """ OVC-017
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. create account with certain limits, should succeed
        #. create 1st cloudspace that doesn't exceed account limits
        #. create 2nd cloudspace that doesn't exceed account limits
        #. create VM on the 1st cloudspace without exceeding account limits , should succeed
        #. create VM on the 2nd cloudspace, should fail (as total VMs Memory and cores exceeds that of the account)
        #. create VM on the 2nd cloudspace, should fail (as total VMs disks capacity exceeds that of the account)
        #. create 2nd VM  on the 2nd cloudspace without exceeding account total limits, should succeed
        #. Add publicip to the 2nd VM, should fail as acoount total IPs=2

        """
        self.lg('- create account with certain limits, should succeed')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email,
                                                          maxMemoryCapacity=12,
                                                          maxVDiskCapacity=250 , maxCPUCapacity=6,
                                                          maxNumPublicIP= 2)
        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

        self.lg('- create 1st cloudspace that doesn\'t exceed account limits')
        cloudspaceId_1 = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=8,
                                                       maxDiskCapacity=130, maxCPUCapacity=4,
                                                       maxNumPublicIP=1)

        self.lg('- create 2st cloudspace that doesn\'t exceed account limits')
        cloudspaceId_2 = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs2', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=4,
                                                       maxDiskCapacity=120, maxCPUCapacity=2,
                                                       maxNumPublicIP=1)

        self.lg('- create VM (M=8, C=4, BD=100, DD=[10,10,10]) on the 1st cloudspace, should succeed')
        self.cloudapi_create_machine(cloudspaceId_1, self.account_owner_api, size_id=4,
                                     disksize=100, datadisks=[10,10,10])

        self.lg('- create VM (M=8, C=4) on the 2nd cloudspace, should fail as T_M=16 & T_C=8')
        try:
            self.cloudapi_create_machine(cloudspaceId_2, self.account_owner_api, size_id=4)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM (M=2, C=2, BD=100, DD=[10,10,10]) on the 2nd cloudspace,'
                ' should fail as T_VD=260')
        try:
            self.cloudapi_create_machine(cloudspaceId_2, self.account_owner_api, size_id=2,
                                         disksize=100, datadisks=[10,10,10])
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create 2nd VM (M=4, C=2, BD=100, DD=[10,10]) on the 2nd cloudspace, should succeed')
        machineId_2 = self.cloudapi_create_machine(cloudspaceId_2, self.account_owner_api, size_id=3,
                                                 disksize=100, datadisks=[10,10])

        self.lg('- Add publicip to the 2nd VM, should fail as T_IPs=2')
        try:
            self.account_owner_api.cloudapi.machines.attachExternalNetwork(machineId=machineId_2)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')



    def test003_resource_limits_on_cloudspace_level(self):
        """ OVC-018
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. create account with certain limits, should succeed
        #. create cloudspace that doesn't exceed account limits
        #. create 1st VM on the created cloudspace without exceeding its limits, should succeed
        #. create another VM on the created cloudspace, should fail (as total VMs Memory and cores exceeds that of the cloudspace)
        #. create another VM on the created cloudspace, should fail (as total VMs disks capacity exceeds that of the cloudspace)
        #. create 2nd VM on the created cloudspace, should succeed
        #. Add publicip to the 2nd VM, should fail as total cloudspace IPs=1

        """
        self.lg('- create account with certain limits, should succeed')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email,
                                                          maxMemoryCapacity=200,
                                                          maxVDiskCapacity=500 , maxCPUCapacity=100,
                                                          maxNumPublicIP= 10)
        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

        self.lg('- create cloudspace that doesn\'t exceed account limits')
        cloudspaceId= self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=20,
                                                       maxDiskCapacity=250, maxCPUCapacity=10,
                                                       maxNumPublicIP=1)

        self.lg('- create 1st VM (M=16, C=8, BD=100, DD=[10,10,10]) on the created cloudspace, should succeed')
        self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=5,
                                     disksize=100, datadisks=[10,10,10])

        self.lg('- create another VM (M=8, C=4) on the created cloudspace, should fail as T_M=24 & T_C=12')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=4)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM (M=2, C=2, BD=100, DD=[10,10,10]) on the created cloudspace,'
                ' should fail as T_VD=260')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=2,
                                         disksize=100, datadisks=[10,10,10])
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create 2nd VM (M=2, C=2, BD=100, DD=[10,10]) on the created cloudspace, should succeed')
        machineId = self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=2,
                                                 disksize=100, datadisks=[10,10])

        self.lg('- Add publicip to the 2nd VM, should fail as T_IPs=1')
        try:
            self.account_owner_api.cloudapi.machines.attachExternalNetwork(machineId=machineId)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')
