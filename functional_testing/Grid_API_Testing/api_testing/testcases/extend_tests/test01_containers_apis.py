import random
import time
import unittest
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.python_client.client import Client
from api_testing.grid_apis.apis.nodes_apis import NodesAPI
from api_testing.grid_apis.apis.containers_apis import ContainersAPI
import json


class TestcontaineridAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.lg.info('Choose one random node of list of running nodes.')
        self.node_id = self.get_random_node()
        if self.node_id is None:
            self.lg.info(' No node found')
            return
        self.node = {}
        for node in self.nodes:
            if node['id'] == self.node_id:
                self.g8os_ip = node['ip']
                self.node = node
                break
        self.g8core = Client(self.g8os_ip)
        self.root_url = "https://hub.gig.tech/deboeckj/flist-lede-17.01.0-r3205-59508e3-x86-64-generic-rootfs.flist"
        self.storage = "ardb://hub.gig.tech:16379"
        self.container_name = self.rand_str()
        self.hostname = self.rand_str()
        self.process_body = {'name': 'yes'}
        self.container_body = {"name": self.container_name, "hostname": self.hostname, "flist": self.root_url,
                               "hostNetworking": False, "initProcesses": [], "filesystems": [],
                               "ports": [], "storage": self.storage
                               }

    def tearDown(self):
        self.lg.info('TearDown:delete all created container ')
        for container in self.createdcontainer:
            self.containers_api.delete_containers_containerid(container['node'],
                                                              container['container'])

    def test001_check_coonection_with_False_hostNetworking(self):
        """ GAT-082
        *Check container internet connection with false hostNetworking options *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Create container with false hostNetworking.
        #. Try to connect to internet from created container ,Should fail.

        """
        self.lg.info('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id=self.node_id, body=self.container_body)
        self.assertEqual(response.status_code, 201)
        self.lg.info('Make sure it running .')
        self.assertTrue(self.wait_for_container_status("running", self.containers_api.get_containers_containerid,
                                                       node_id=self.node_id,
                                                       container_id=self.container_name))
        self.createdcontainer.append({"node": self.node_id, "container": self.container_name})

        self.lg.info("Try to connect to internet from created container ,Should fail.")
        container = self.g8core.get_container_client(self.container_name)
        self.assertTrue(container)
        response = container.bash('ping -c 5 google.com').get()
        self.assertEqual(response.state, 'ERROR')

    def test002_check_coonection_with_True_hostNetworking(self):
        """ GAT-083
        *Check container internet connection with true hostNetworking options *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Create container with True hostNetworking.
        #. Try to connect to internet from created container ,Should succeed.

        """
        self.container_body['hostNetworking']=True

        self.lg.info('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id=self.node_id, body=self.container_body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Make sure it is running .')
        self.assertTrue(self.wait_for_container_status("running", self.containers_api.get_containers_containerid,
                                                       node_id=self.node_id,
                                                       container_id=self.container_name))
        self.createdcontainer.append({"node": self.node_id, "container": self.container_name})

        self.lg.info("Try to connect to internet from created container ,Should succeed.")
        container = self.g8core.get_container_client(self.container_name)
        self.assertTrue(container)
        response = container.bash('ping -c 5 google.com').get()
        self.assertEqual(response.state, 'SUCCESS')
        self.assertNotIn("unreachable", response.stdout)

    def test003_create_container_with_init_process(self):
        """ GAT-084
        *Check that container created with init process *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Create container with initProcess.
        #. Check that container created with init process.

        """
        self.container_body['flist']="https://hub.gig.tech/dina_magdy/initprocess.flist"
        ## flist which have script which print environment varaibles and print stdin
        Environmentvaraible = "MYVAR=%s"%self.rand_str()
        stdin = self.rand_str()
        self.container_body['initProcesses'] = [{"name": "sh", "pwd": "/",
                                                 "args": ["sbin/process_init"],
                                                 "environment":["%s"%Environmentvaraible],
                                                 "stdin":"%s"%stdin}]

        self.lg.info('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id=self.node_id, body=self.container_body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Make sure it running')
        self.assertTrue(self.wait_for_container_status("running", self.containers_api.get_containers_containerid,
                                                       node_id=self.node_id,
                                                       container_id=self.container_name))
        self.createdcontainer.append({"node": self.node_id, "container": self.container_name})

        self.lg.info("Check that container created with init process.")
        container = self.g8core.get_container_client(self.container_name)
        response = container.bash("ls |grep  out.text").get()
        self.assertEqual(response.state, "SUCCESS")
        response = container.bash("cat out.text | grep %s"%stdin).get()
        self.assertEqual(response.state, "SUCCESS", "init processes didn't get stdin correctly")
        response = container.bash("cat out.text | grep %s"%Environmentvaraible).get()
        self.assertEqual(response.state, "SUCCESS", "init processes didn't get Env varaible  correctly")

    def test004_create_containers_with_different_flists(self):
        """ GAT-085
        *create contaner with different flists *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random flist .
        #. Create container with this flist, Should succeed.
        #. Make sure it created with required values, should succeed.
        #. Make sure that created container is running,should succeed.
        #. Check that container created on node, should succeed
        """
        flistslist = ["ovs.flist", "ubuntu1604.flist", "grid-api-flistbuild.flist",
                      "cloud-init-server-master.flist"]

        flist = random.choice(flistslist)
        self.container_body['flist']="https://hub.gig.tech/gig-official-apps/%s"%flist
        self.lg.info('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id=self.node_id, body=self.container_body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Make sure it created with required values and running, should succeed.')
        self.assertTrue(self.wait_for_container_status("running", self.containers_api.get_containers_containerid,
                                                       node_id=self.node_id,
                                                       container_id=self.container_name))
        self.createdcontainer.append({"node": self.node_id, "container": self.container_name})
        response = self.containers_api.get_containers_containerid(self.node_id, self.container_name)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        for key in response_data.keys():
            if key == 'initprocesses':
                self.assertEqual(response_data[key], self.container_body['initProcesses'])
                continue
            if key in self.container_body.keys():
                self.assertEqual(response_data[key], self.container_body[key])

        self.lg.info("check that container created on node, should succeed")
        self.assertTrue(self.g8core.client.container.find(self.container_name))


    @unittest.skip("https://github.com/g8os/core0/issues/228")
    def test005_Check_container_access_to_host_dev(self):
        """ GAT-086
        *Make sure that container doesn't have access to host dev files *

        **Test Scenario:**

        #. Create container, Should succeed.
        #. Make sure that created container is running,should succeed.
        #. Check that container doesn't has access to host dev files .

        """

        self.lg.info('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id=self.node_id, body=self.container_body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Make sure it created with required values and running, should succeed.')
        self.assertTrue(self.wait_for_container_status("running", self.containers_api.get_containers_containerid,
                                                       node_id=self.node_id,
                                                       container_id=self.container_name))
        self.createdcontainer.append({"node": self.node_id, "container": self.container_name})

        self.lg.info("Check that container doesn't has access to host dev files .")
        container = self.g8core.get_container_client(self.container_name)
        response = container.bash("ls -alh").get().stdout
        for line in response.splitlines():
            if "dev" in line:
                self.assertNotIn('w', line)
