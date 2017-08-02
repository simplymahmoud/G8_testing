import g8core
import time


class Client:
    def __init__(self, ip):
        self.client = g8core.Client(ip)

    def stdout(self, resource):
        return resource.get().stdout.replace('\n', '').lower()

    def get_nodes_cpus(self):
        info = self.client.info.cpu()
        cpuInfo = []
        for processor in info:
            cpuInfo.append(processor)
        return cpuInfo

    def get_nodes_nics(self):
        r = self.client.bash('ip -br a').get().stdout
        nics = [x.split()[0] for x in r.splitlines()]
        nicInfo = []
        for nic in nics:
            if '@' in nic:
                nic = nic[:nic.index('@')]
            addrs = self.client.bash('ip -br a show "{}"'.format(nic)).get()
            addrs = addrs.stdout.splitlines()[0].split()[2:]
            mtu = int(self.stdout(self.client.bash('cat /sys/class/net/{}/mtu'.format(nic))))
            hardwareaddr = self.stdout(self.client.bash('cat /sys/class/net/{}/address'.format(nic)))
            if hardwareaddr == '00:00:00:00:00:00':
                    hardwareaddr = ''
            addrs = [ x for x in addrs]
            if addrs == [] :
                addrs= None
            tmp = {"name": nic, "hardwareaddr": hardwareaddr, "mtu": mtu, "addrs": addrs}
            nicInfo.append(tmp)

        return nicInfo

    def get_node_bridges(self):
        bridgesInfo = []
        nics = self.client.bash('ls /sys/class/net').get().stdout.splitlines()
        for nic in nics:
            status = self.client.bash('cat /sys/class/net/{}/operstate'.format(nic)).get().stdout.strip()
            bridge = {"name":nic, "status":status}
            bridgesInfo.append(bridge)

        return bridgesInfo

    def get_nodes_mem(self):
        lines = self.client.bash('cat /proc/meminfo').get().stdout.splitlines()
        memInfo = {'available': 0, 'buffers': 0, 'cached': 0,
                    'inactive': 0, 'total': 0}
        for line in lines:
            line = line.replace('\t', '').strip()
            key = line[:line.find(':')].lower()
            value = line[line.find(':')+2:line.find('kB')].strip()
            if 'mem' == key[:3]:
                key = key[3:]
            if key in memInfo.keys():

                memInfo[key] = int(value)*1024
        return memInfo

    def get_nodes_info(self):
        hostname = self.client.system('uname -n').get().stdout.strip()
        krn_name = self.client.system('uname -s').get().stdout.strip().lower()
        return {"hostname":hostname, "os":krn_name}

    def get_nodes_disks(self):
        diskInfo = []
        diskInfo_format = {'mountpoint':"", 'fstype': "", 'device': [], 'size': 0}
        response = self.client.disk.list()
        disks = response['blockdevices']
        for disk in disks:
            item = dict(diskInfo_format)
            if disk['mountpoint']:
                item['mountpoint'] = disk['mountpoint']

            if disk['fstype']!= None:
                item['fstype'] = disk['fstype']

            item['device'] = '/dev/%s'%disk['name']

            if int(disk['size']) >= 1073741824:
                item['size'] = int(int(disk['size'])/(1024*1024*1024))
            diskInfo.append(item)
        return diskInfo

    def get_jobs_list(self):
        jobs = self.client.job.list()
        gridjobs = []
        temp = {}
        for job in jobs:
            temp['id'] = job['cmd']['id']
            if job['cmd']['arguments']:
                if ('name' in job['cmd']['arguments'].keys()):
                    temp['name'] = job['cmd']['arguments']['name']
            temp['starttime'] = job['starttime']
            gridjobs.append(temp)
        return gridjobs

    def get_node_state(self):
        state = self.client.json('core.state', {})
        del state['cpu']
        return state

    def start_job(self):
        job_id = self.client.system("tailf /etc/nsswitch.conf").id
        jobs = self.client.job.list()
        for job in jobs:
            if job['cmd']['id'] == job_id:
                return job_id
        return False

    def start_process(self):
        self.client.system("tailf /etc/nsswitch.conf")
        processes = self.get_processes_list()
        for process in processes:
            if process['cmdline'] == "tailf /etc/nsswitch.conf":
                return process['pid']
        return False

    def getFreeDisks(self):
        freeDisks = []
        disks = self.client.disk.list()['blockdevices']
        for disk in disks:
            if not disk['mountpoint'] and disk['kname'] != 'sda':
                if 'children' not in disk.keys():
                    freeDisks.append('/dev/{}'.format(disk['kname']))
                else:
                    for children in disk['children']:
                        if children['mountpoint']:
                            break
                    else:
                        freeDisks.append('/dev/{}'.format(disk['kname']))

        return freeDisks

    def get_processes_list(self):
        processes = self.client.process.list()
        return processes

    def get_container_client(self,container_name):
        container = self.client.container.find(container_name)
        if not container:
            return False
        container_id = list(container.keys())[0]
        container_client = self.client.container.client(int(container_id))
        return container_client

    def get_container_info(self, container_id):
        container = (self.client.container.find(container_id))
        if not container:
            return False
        container_id=list(container.keys())[0]
        container_info = {}
        golden_data = self.client.container.list().get(str(container_id), None)
        if not golden_data:
            return False
        golden_value = golden_data['container']
        container_info['nics'] = ([{i: nic[i] for i in nic if i != 'hwaddr'} for nic in golden_value['arguments']['nics']])
        container_info['ports'] = (['%s:%s' % (key, value) for key, value in golden_value['arguments']['port'].items()])
        container_info['hostNetworking'] = golden_value['arguments']['host_network']
        container_info['hostname'] = golden_value['arguments']['hostname']
        container_info['flist'] = golden_value['arguments']['root']
        container_info['storage'] = golden_value['arguments']['storage']
        return container_info

    def get_container_job_list(self, container_name):
        container_id = list(self.client.container.find(container_name).keys())[0]
        golden_values = []
        container = self.client.container.client(int(container_id))
        container_data = container.job.list()
        # cannot compare directly as the job.list is considered a job and has a different id everytime is is called
        for i, golden_value in enumerate(container_data[:]):
            if golden_value.get('command', "") == 'job.list':
                container_data.pop(i)
                continue
            golden_values.append((golden_value['cmd']['id'], golden_value['starttime']))
        return set(golden_values)

    def wait_on_container_update(self, container_name, timeout, removed):
        for _ in range(timeout):
            if removed:
                if not self.client.container.find(container_name):
                    return True
            else:
                if self.client.container.find(container_name):
                    return True
            time.sleep(1)
        return False

    def wait_on_container_job_update(self, container_name, job_id, timeout, removed):
        container_id = int(list(self.client.container.find(container_name).keys())[0])
        container = self.client.container.client(container_id)
        for _ in range(timeout):
            if removed:
                if job_id not in [item['cmd']['id']for item in container.job.list()]:
                    return True
            else:
                if job_id in [item['cmd']['id']for item in container.job.list()]:
                    return True
            time.sleep(1)
        return False
