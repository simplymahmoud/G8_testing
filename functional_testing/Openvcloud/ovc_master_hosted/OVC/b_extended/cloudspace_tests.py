# coding=utf-8
import random

from ....utils.utils import BasicACLTest

from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError

class CloudspaceTests(BasicACLTest):

    def setUp(self):
        super(CloudspaceTests, self).setUp()
        self.default_setup()

    def test001_validate_deleted_cloudspace_with_running_machines(self):
        """ OVC-020
        *Test case for validate deleted cloudspace with running machines get destroyed.*

        **Test Scenario:**

        #. Create 3+ vm's possible with different images on new cloudspace, should succeed
        #. Cloudspace status should be DEPLOYED, should succeed
        #. Try to delete the cloudspace with delete, should fail with 409 conflict
        #. Delete the cloudspace with destroy, should succeed
        #. Try list user's cloud spaces, should return empty list, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg("1- Create 3+ vm's possible with different images on new cloudspace, "
                "should succeed")
        cloudspace_id = self.cloudapi_cloudspace_create(self.account_id,
                                                        self.location,
                                                        self.account_owner)

        images = self.api.cloudapi.images.list()
        for image in images:
            image_name = image['name']
            self.lg('- using image [%s]' % image_name)
            size = random.choice(self.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id))
            self.lg('- using image [%s] with memory size [%s]' % (image_name, size['memory']))
            if 'Windows' in image_name:
                   while True:
                       disksize = random.choice(size['disks'])
                       if disksize > 25:
                            break
            else:
                disksize = random.choice(size['disks'])
            self.lg('- using image [%s] with memory size [%s] with disk '
                    '[%s]' % (image_name, size['memory'], disksize))
            machine_id = self.cloudapi_create_machine(cloudspace_id=cloudspace_id,
                                                      size_id=size['id'],
                                                      image_id=image['id'],
                                                      disksize=disksize)

        self.lg("2- Cloudspace status should be DEPLOYED, should succeed")
        self.wait_for_status(status='DEPLOYED', func=self.api.cloudapi.cloudspaces.get,
                             timeout=60, cloudspaceId=cloudspace_id)

        self.lg('3- Try to delete the cloudspace with delete, should fail with 409 conflict')
        try:
            self.api.cloudapi.cloudspaces.delete(cloudspaceId=cloudspace_id)
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 409)

        self.lg('4- Delete the cloudspace with destroy, should succeed')
        self.api.cloudbroker.cloudspace.destroy(accountId= self.account_id,
                                                cloudspaceId=cloudspace_id,
                                                reason='test')
        self.wait_for_status('DESTROYED', self.api.cloudapi.cloudspaces.get,
                             cloudspaceId=cloudspace_id)

        self.lg("5- Try list user's cloud spaces, should return empty list, should succeed")
        self.assertFalse(self.api.cloudapi.machines.list(cloudspaceId=cloudspace_id))

        self.lg('%s ENDED' % self._testID)