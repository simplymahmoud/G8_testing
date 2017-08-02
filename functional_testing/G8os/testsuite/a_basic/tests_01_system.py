from utils.utils import BaseTest
import time
import unittest
from nose_parameterized import parameterized
import os
import io


class SystemTests(BaseTest):

    def setUp(self):

        super(SystemTests, self).setUp()
        self.check_g8os_connection(SystemTests)

    def get_permission(self, client, path):
        return int(self.stdout(client.bash('stat -c %a {}'.format(path))))

    def container_create(self):
        self.cid = self.create_container(root_url=self.root_url, storage=self.storage)
        self.client_container = self.client.container.client(self.cid)

    def remove_container(self):
        self.client.container.terminate(self.cid)

    def getNicInfo(self, client):
        r = client.bash('ip -br a').get().stdout
        nics = [x.split()[0] for x in r.splitlines()]
        nicInfo = []
        for nic in nics:
            if '@' in nic:
                nic = nic[:nic.index('@')]
            addrs = client.bash('ip -br a show "{}"'.format(nic)).get().stdout.splitlines()[0].split()[2:]
            mtu = int(self.stdout(client.bash('cat /sys/class/net/{}/mtu'.format(nic))))
            hardwareaddr = self.stdout(client.bash('cat /sys/class/net/{}/address'.format(nic)))
            if hardwareaddr == '00:00:00:00:00:00':
                    hardwareaddr = ''
            tmp = {"name": nic, "hardwareaddr": hardwareaddr, "mtu": mtu, "addrs": [{"addr": x} for x in addrs]}
            nicInfo.append(tmp)

        return nicInfo

    def getCpuInfo(self, client):
        lines = client.bash('cat /proc/cpuinfo').get().stdout.splitlines()
        cpuInfo = {'vendorId': [], 'family': [], 'stepping': [], 'cpu': [], 'coreId': [], 'model': [],
                    'cacheSize': [], 'cores': [], 'flags': [], 'modelName': [], 'physicalId':[]}

        mapping = { "vendor_id": "vendorId", "cpu family": "family", "processor": "cpu", "core id": "coreId",
                    "cache size": "cacheSize", "cpu cores": "cores", "model name": "modelName", "physical id": "physicalId",
                    "stepping": "stepping", "flags": "flags", "model": "model"}

        keys = mapping.keys()
        for line in lines:
            line = line.replace('\t', '')
            for key in keys:
                if key == line[:line.find(':')]:
                    item = line[line.index(':') + 1:].strip()
                    if key in ['processor', 'stepping', 'cpu cores']:
                        item = int(item)
                    if key == 'cache size':
                        item = int(item[:item.index(' KB')])
                    if key == 'flags':
                        item = item.split(' ')
                    cpuInfo[mapping[key]].append(item)

        return cpuInfo

    def getDiskInfo(self, client):
        diskInfo = {'mountpoint': [], 'fstype': [], 'device': [], 'opts': []}
        response = client.bash('mount').get().stdout
        lines = response.splitlines()
        for line in lines:
            line = line.split()
            diskInfo['mountpoint'].append(line[2])
            diskInfo['fstype'].append(line[4])
            diskInfo['device'].append(line[0])
            diskInfo['opts'].append(line[5][1:-1])

        return diskInfo

    def getMemInfo(self, client):

        lines = client.bash('cat /proc/meminfo').get().stdout.splitlines()
        memInfo = { 'active': 0, 'available': 0, 'buffers': 0, 'cached': 0,
                    'free': 0,'inactive': 0, 'total': 0}

        mapping = { 'Active': 'active', 'MemAvailable': 'available', 'Buffers':'buffers',
                    'Cached': 'cached', 'MemFree': 'free', 'Inactive':'inactive', 'MemTotal':'total'}

        keys = mapping.keys()
        for line in lines:
            line = line.replace('\t', '')
            for key in keys:
                if key == line[:line.find(':')]:
                    item = int(line[line.index(':') + 1:line.index(' kB')].strip())
                    item = item * 1024
                    memInfo[mapping[key]] = item

        return memInfo

    def test001_execute_commands(self):

        """ g8os-001
        *Test case for testing basic commands using  bash and system*

        **Test Scenario:**
        #. Check if you can ping the remote host, should succeed
        #. Create folder using system
        #. Check that the folder is created using bash (C1)
        #. Check that you can get same responce for (C1)
        #. Remove the created folder
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Check if you can ping the remote host, should succeed')
        rs = self.client.ping()
        self.assertEqual(rs[:4], 'PONG')

        self.lg('Create folder using system')
        folder = self.rand_str()
        self.client.system('mkdir {}'.format(folder))

        self.lg('Check that the folder is created')
        rs1 = self.client.bash('ls | grep {}'.format(folder))
        rs_ob = rs1.get()
        self.assertEqual(rs_ob.stdout, '{}\n'.format(folder))
        self.assertEqual(rs_ob.state, 'SUCCESS')

        self.lg('Check that you can get same responce for (C1)')
        rs11 = self.client.response_for(rs1.id)
        self.assertEqual(self.stdout(rs11), self.stdout(rs1))
        self.assertEqual(rs1.id, rs11.id)

        self.lg('Remove the created folder')
        self.client.bash('rm -rf {}'.format(folder))
        time.sleep(0.5)
        rs2 = self.client.bash('ls | grep {}'.format(folder))
        self.assertEqual(self.stdout(rs2), '')

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug: https://github.com/g8os/core0/issues/254')
    def test002_kill_list_processes(self):

        """ g8os-002
        *Test case for testing killing and listing processes*

        **Test Scenario:**
        #. Create process that runs for long time using both system and bash
        #. List the process, should be found
        #. Kill the process
        #. List the process, shouldn't be found
        """

        self.lg('{} STARTED'.format(self._testID))

        cmd = 'sleep 40'
        self.client.bash(cmd)
        self.lg('Created process that runs for long time using {}'.format(cmd))

        self.lg('List the process, should be found')
        id = self.get_process_id(cmd)
        self.assertIsNotNone(id)

        self.lg('Kill the process')
        self.client.process.kill(id)

        self.lg('List the process, shouldn\'t be found')
        id = self.get_process_id(cmd)
        self.assertIsNone(id)

        self.lg('{} ENDED'.format(self._testID))

    @parameterized.expand(['client', 'container'])
    def test003_os_info(self, client_type):

        """ g8os-003
        *Test case for checking on the system os information*

        **Test Scenario:**
        #. Get the os information using g8os/container client
        #. Get the hostname and compare it with the g8os/container os insformation
        #. Get the kernal's name and compare it with the g8os/container os insformation
        """

        self.lg('{} STARTED'.format(self._testID))

        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('Get the os information using g8os/container client')
        os_info = client.info.os()

        self.lg('Get the hostname and compare it with the g8os/container os insformation')
        hostname = client.system('uname -n').get().stdout.strip()
        self.assertEqual(os_info['hostname'], hostname)

        self.lg('Get the kernal\'s name and compare it with the g8os/container os insformation')
        krn_name = client.system('uname -s').get().stdout.strip()
        self.assertEqual(os_info['os'], krn_name.lower())

        self.lg('{} ENDED'.format(self._testID))

    @parameterized.expand(['client', 'container'])
    def test004_mem_info(self, client_type):

        """ g8os-004
        *Test case for checking on the system memory information*

        **Test Scenario:**
        #. Get the memory information using g8os/container client
        #. Get the memory information using bash
        #. Compare memory g8os/container  results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('get memory info using bash')
        expected_mem_info = self.getMemInfo(client)

        self.lg('get memory info using g8os/container ')
        g8os_mem_info = client.info.mem()

        self.lg('compare g8os/container  results to bash results')
        self.assertEqual(expected_mem_info['total'], g8os_mem_info['total'])
        params_to_check = ['active', 'available', 'buffers', 'cached', 'free', 'inactive']
        for key in params_to_check:
            threshold = 1024 * 1000  # acceptable threshold (1 MB)
            g8os_value = g8os_mem_info[key]
            expected_value = expected_mem_info[key]
            self.assertTrue(expected_value - threshold <= g8os_value <= expected_value + threshold, key)

        self.lg('{} ENDED'.format(self._testID))

    @parameterized.expand(['client', 'container'])
    def test005_cpu_info(self, client_type):

        """ g8os-005
        *Test case for checking on the system CPU information*

        **Test Scenario:**
        #. Get the CPU information using g8os/container client
        #. Get the CPU information using bash
        #. Compare CPU g8os/container  results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('get cpu info using bash')
        expected_cpu_info = self.getCpuInfo(client)

        self.lg('get cpu info using g8os')
        g8os_cpu_info = client.info.cpu()

        self.lg('compare g8os/container results to bash results')
        for key in expected_cpu_info.keys():
            if key == 'cores':
                continue
            g8os_param_list = [x[key] for x in g8os_cpu_info]
            self.assertEqual(expected_cpu_info[key], g8os_param_list)

        self.lg('{} ENDED'.format(self._testID))

    @parameterized.expand(['client', 'container'])
    def test006_disk_info(self, client_type):

        """ g8os-006
        *Test case for checking on the disks information*

        **Test Scenario:**
        #. Get the disks information using g8os client
        #. Get the disks information using bas
        #. Compare disks g8os results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('get disks info using linux bash command (mount)')
        expected_disk_info = self.getDiskInfo(client)

        self.lg('get cpu info using g8os')
        g8os_disk_info = client.info.disk()

        self.lg('compare g8os results to bash results')
        for key in expected_disk_info.keys():
            g8os_param_list = [x[key] for x in g8os_disk_info]
            self.assertEqual(expected_disk_info[key], g8os_param_list)

        self.lg('{} ENDED'.format(self._testID))

    def test007_nic_info(self):

        """ g8os-007
        *Test case for checking on the system nic information*

        **Test Scenario:**
        #. Get the nic information using g8os client
        #. Get the information using bash
        #. Compare nic g8os results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('get nic info using linux bash command (ip a)')
        expected_nic_info = self.getNicInfo(self.client)

        self.lg('get nic info using g8os client')
        g8os_nic_info = self.client.info.nic()

        self.lg('compare g8os/container results to bash results')
        params_to_check = ['name', 'addrs', 'mtu', 'hardwareaddr']
        for i in range(len(expected_nic_info) - 1):
            for param in params_to_check:
                self.assertEqual(expected_nic_info[i][param], g8os_nic_info[i][param])

        self.lg('{} ENDED'.format(self._testID))

    @parameterized.expand(['client', 'container'])
    def test008_mkdir_exists_list_chmod_move_remove_directory(self, client_type):
        """ g8os-015
        *Test case for test filesystem mkdir, exists, list, chmod, move, remove methods*

        **Test Scenario:**
        #. Make new directory (D1), should succeed
        #. Check directory (D1) exists, should succeed
        #. Move directory (D1), should succeed
        #. Remove directory (D1), should succeed
        #. Make new parent directory (D2), should succeed
        #. Make new directory (D3) inside (D2), should succeed
        #. Change directory (D2) mode, should succeed
        """
        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Make new directory (D1), should succeed')
        dir_name = self.rand_str()
        client.filesystem.mkdir(dir_name)

        self.lg('Check directory (D1) is exists, should succeed')
        ## using bash
        ls = client.bash('ls').get().stdout.splitlines()
        self.assertIn(dir_name, ls)
        ## using bash filesystem.list
        ls = [x['name'] for x in client.filesystem.list('.')]
        self.assertIn(dir_name, ls)
        ## using bash filesystem.exists
        self.assertTrue(client.filesystem.exists(dir_name))

        self.lg('Move directory (D1), should succeed')
        new_destination = '/root/{}'.format(dir_name)
        client.filesystem.move(dir_name, new_destination)
        self.assertTrue(client.filesystem.exists(new_destination))
        self.assertFalse(client.filesystem.exists(dir_name))

        self.lg('Remove directory (D1), should succeed')
        client.filesystem.remove(new_destination)
        ls = client.bash('ls').get().stdout.splitlines()
        self.assertNotIn(dir_name, ls)

        self.lg('Make new parent directory (D2), should succeed')
        parent_dir = self.rand_str()
        client.filesystem.mkdir(parent_dir)

        self.lg('Make new directory (D3) inside (D2), should succeed')
        child_dir = '{}/{}'.format(parent_dir, self.rand_str())
        client.filesystem.mkdir(child_dir)

        self.lg('Change directory (D2) mode, should succeed')
        client.filesystem.chmod(parent_dir, 0o777)
        parent_dir_perimission = self.get_permission(client, parent_dir)
        child_dir_perimission = self.get_permission(client, child_dir)
        self.assertEqual(parent_dir_perimission, 777)
        self.assertNotEqual(child_dir_perimission, 777)

        self.lg('Change directory (D2) mode recursively, should succeed')
        client.filesystem.chmod(parent_dir, 0o321, recursive=True)
        parent_dir_perimission = self.get_permission(client, parent_dir)
        child_dir_perimission = self.get_permission(client, child_dir)
        self.assertEqual(parent_dir_perimission, 321)
        self.assertEqual(child_dir_perimission, 321)

        if client_type == 'container':
            self.remove_container()

        self.lg('{} ENDED'.format(self._testID))


    @parameterized.expand(['client', 'container'])
    def test009_open_close_read_write_file(self, client_type):

        """ g8os-019
        *Test case for test filesystem upload, download, upload_file, download_file methods*

        **Test Scenario:**
        #. Open file (F1) in read (r) mode, should succeed
        #. Read file (F1) and check its content, should succeed
        #. Try to write to the file (F1), should fail
        #. Open file (F1) in (w+) mode
        #. Write text to file (F1), should succeed
        #. Check file (F1) is truncated and contains only (T2) text
        #. Try to read the file (F1), should fail
        #. Open file (F1) in (w+) mode
        #. Write text to file (F1), should succeed
        #. Read text from file (F1), should succeed
        #. Open file (F1) in (r+) mode
        #. Write text to file (F1), should success
        #. Check file (F1) content, should success
        #. Open file (F1) in (a) mode
        #. Write text to file (F1), should succeed
        #. Check file (F1) text , should succeed
        #. Create file (F2) using open in (x) mode, should succeed
        #. Check if  file (F2) exists, should succeed
        """

        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('{} STARTED'.format(self._testID))

        file_name = '{}.txt'.format(self.rand_str())
        client.bash('touch /{}'.format(file_name))
        time.sleep(1)

        open_modes = ['r', 'w', 'a', 'w+', 'r+', 'a+', 'x']
        for mode in open_modes:
            if mode != 'x':
                txt = 'line1\nline2\nline3'
                client.bash('echo "{}" > {}'.format(txt, file_name))
                time.sleep(1)
                f = client.filesystem.open(file_name, mode=mode)

            if mode == 'r':

                self.lg('Open file (F1) in read (r) mode, should succeed')

                self.lg('Read file (F1) and check its content, should succeed')
                file_text = client.filesystem.read(f).decode('utf-8')
                self.assertEqual(file_text, '{}\n'.format(txt))

                self.lg('Try to write to the file (F1), should fail')
                txt = new_txt = str.encode(self.rand_str())
                with self.assertRaises(RuntimeError):
                    client.filesystem.write(f, txt)
                with self.assertRaises(RuntimeError):
                    client.filesystem.open(self.rand_str(), mode=mode)

            if mode == 'w':

                self.lg('Open file (F1) in write only (w) mode')

                self.lg('Write text (T2) to file')
                new_txt = str.encode(self.rand_str())
                client.filesystem.write(f, new_txt)

                self.lg('Check file (F1) is truncated and contains only (T2) text')
                file_text = client.bash('cat {}'.format(file_name)).get().stdout
                self.assertEqual(file_text, '{}\n'.format(new_txt.decode('utf-8')), mode)

                self.lg('Try to read the file (F1), should fail')
                with self.assertRaises(RuntimeError):
                    client.filesystem.read(f)

            if mode == 'w+':

                self.lg('Open file (F1) in (w+) mode')

                self.lg('Write text to file (F1), should succeed')
                new_txt = str.encode(self.rand_str())
                client.filesystem.write(f, new_txt)

                self.lg('Read text from file (F1), should succeed')
                client.filesystem.read(f)

            # read/write(at begin)
            if mode == 'r+':

                self.lg('Open file (F1) in (r+) mode')

                self.lg('Write text to file (F1), should success')
                new_txt = str.encode(self.rand_str())
                l = len(new_txt)
                client.filesystem.write(f, new_txt)

                self.lg('Check file (F1) content, should success')
                file_text = client.bash('cat {}'.format(file_name)).get().stdout
                self.assertEqual(file_text, '{}{}\n'.format(new_txt.decode('utf-8'), txt[l:]))
                file_text = client.filesystem.read(f).decode('utf-8')
                self.assertEqual(file_text, '{}\n'.format(txt[l:]))
                with self.assertRaises(RuntimeError):
                    client.filesystem.open(self.rand_str(), mode=mode)

            if mode == 'a':

                self.lg('Open file (F1) in (a) mode')

                self.lg('Write text to file (F1), should succeed')
                new_txt = str.encode(self.rand_str())
                client.filesystem.write(f, new_txt)
                file_text = client.bash('cat {}'.format(file_name)).get().stdout

                self.lg('Check file (F1) text , should succeed')
                self.assertEqual(file_text, '{}\n{}\n'.format(txt, new_txt.decode('utf-8')))

            if mode == 'x':
                self.lg('Create file (F2) using open in (x) mode, should succeed')
                file_name_2 = '{}.txt'.format(self.rand_str())
                client.filesystem.open(file_name_2, mode=mode)

                self.lg('Check if  file (F2) exists, should succeed')
                ls = client.bash('ls').get().stdout.splitlines()
                self.assertIn(file_name_2, ls)

            client.filesystem.close(f)

        if client_type == 'container':
            self.remove_container()

        self.lg('{} ENDED'.format(self._testID))


    @parameterized.expand(['client', 'container'])
    def test010_upload_download_file(self, client_type):

        """ g8os-018
        *Test case for test filesystem upload, download, upload_file, download_file methods*

        **Test Scenario:**
        #. Create local file (LF1) and write data to it, should succeed
        #. Upload file (LF1) to g8os/container
        #. Check file (LF1) exists in g8os/container and check its data
        #. Upload buffer data to the remote file
        #. Check the remote file content equal to buffer content
        #. Create remote file (RF1) and write data to it, should succeed
        #. Download file (RF1) to localhost
        #. Check file (RF1) exists in localhost and check its data
        #. Download file (RF1) to buffer
        #. Check buffer data equal to file (RF1) content
        """

        if client_type == 'client':
            client = self.client
        else:
            self.container_create()
            client = self.client_container

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create local file (LF1) and write data to it, should succeed')
        local_file_name = '{}.txt'.format(self.rand_str())
        remote_file_name = '{}.txt'.format(self.rand_str())

        test_txt = self.rand_str()
        with open(local_file_name, 'w+') as f:
            f.write(test_txt)

        self.lg('Upload file (LF1) to g8os/container')
        client.filesystem.upload_file('/{}'.format(remote_file_name), local_file_name)

        self.lg('Check file (LF1) is exists in g8os/container and check its data')
        ls = client.bash('ls').get().stdout.splitlines()
        self.assertIn(remote_file_name, ls)
        file_text = client.bash('cat {}'.format(remote_file_name)).get().stdout.strip()
        self.assertEqual(file_text, test_txt)

        self.lg('Upload buffer data to the remote file')
        client.bash('echo "" > {}'.format(remote_file_name))
        buff = io.BytesIO(bytes(self.rand_str().encode('utf-8')))
        client.filesystem.upload('/{}'.format(remote_file_name), buff)

        self.lg('Check the remote file content equal to buffer content')
        file_text = client.bash('cat {}'.format(remote_file_name)).get().stdout.strip()
        self.assertEqual(buff.getvalue().decode('utf-8'), file_text)

        self.lg('Create remote file (RF1) and write data to it, should succeed')
        remote_file_name = '{}.txt'.format(self.rand_str())
        local_file_name = '{}.txt'.format(self.rand_str())
        test_txt = self.rand_str()
        client.bash('echo "{}" > {}'.format(test_txt, remote_file_name))

        self.lg('Download file (RF1) to localhost')
        client.filesystem.download_file('/{}'.format(remote_file_name), local_file_name)

        self.lg('Check file (RF1) is exists in localhost and check its data')
        ls = os.listdir()
        self.assertIn(local_file_name, ls)
        with open(local_file_name, 'r') as f:
            self.assertEqual(f.read().strip(), test_txt)

        self.lg('Download file (RF1) to buffer')
        buff = io.BytesIO()
        client.filesystem.download('/{}'.format(remote_file_name), buff)

        self.lg('Check buffer data equal to file (RF1) content')
        self.assertEqual(buff.getvalue().decode('utf-8').strip(), test_txt)

        if client_type == 'container':
            self.remove_container()

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug: https://github.com/g8os/core0/issues/255')
    def test011_kill_list_jobs(self):

        """ g8os-032
        *Test case for testing killing and listing jobs*

        **Test Scenario:**
        #. Create job that runs for long time
        #. List the job, should be found
        #. Kill the job
        #. List the job, shouldn't be found
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create job that runs for long time')
        cmd = 'core.system'
        match = 'sleep'
        self.client.system('sleep 40')

        self.lg('List the job, should be found')
        id = self.get_job_id(cmd, match)
        self.assertIsNotNone(id)

        self.lg('Kill the job')
        self.client.job.kill(id)

        self.lg('List the job, shouldn\'t be found')
        id = self.get_job_id(cmd, match)
        self.assertIsNone(id)

        self.lg('{} ENDED'.format(self._testID))
