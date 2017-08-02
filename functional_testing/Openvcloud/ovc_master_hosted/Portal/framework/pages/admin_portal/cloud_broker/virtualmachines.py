from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import leftNavigationMenu
import uuid
import time

class virtualmachines():
    def __init__(self, framework):
        self.framework = framework
        self.LeftNavigationMenu = leftNavigationMenu(framework)

    def get_it(self):
        self.LeftNavigationMenu.CloudBroker.VirtualMachines()

    def is_at(self):
        for temp in range(5):
            if 'Virtual Machines' in self.framework.driver.title:
                return True
            else:
                time.sleep(0.5)
        else:
            return False

    def create_virtual_machine(self, cloudspace='', machine_name='', image='', memory='', disk=''):
        cloudspace = cloudspace
        machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
        self.framework.image = image or 'Ubuntu 16.04 x64'
        self.framework.memory = memory or '1024 MB'
        self.framework.disk = disk or '50 GB'

        self.framework.lg('open the cloudspace page')
        self.framework.CloudSpaces.open_cloudspace_page(cloudspace)

        self.framework.lg('add virtual machine')
        self.framework.click('add_virtual_machine')
        self.framework.assertEqual(self.framework.get_text('create_virtual_machine_on_cpu_node'),
                                   'Create Machine On CPU Node')

        self.framework.lg('enter the machine name')
        self.framework.set_text('machine_name_admin', machine_name)

        self.framework.lg('enter the machien description')
        self.framework.set_text('machine_description_admin', str(uuid.uuid4()).replace('-', '')[0:10])

        self.framework.lg('select the image')
        self.framework.select('machine_images_list', self.framework.image)

        self.framework.lg('select the memory')
        self.framework.select('machine_memory_list', self.framework.memory)

        self.framework.lg('select the disk')
        self.framework.select('machine_disk_list', self.framework.disk)

        self.framework.lg('create machine confirm button')
        self.framework.click('machine_confirm_button')

        self.framework.assertTrue(self.framework.check_element_is_exist('virtual machine search'),
                                  "FAIL: Can't create virtual machine")
        self.framework.wait_until_element_attribute_has_text('create_vm_dialog', 'style', 'display: none;')
        self.framework.get_page(self.framework.driver.current_url)
        self.framework.set_text('virtual machine search', machine_name)
        self.framework.wait_until_element_located_and_has_text("virtual_machine_table_first_element",
                                                               machine_name)

    def open_virtual_machine_page(self, cloudspace='', machine_name=''):
        cloudspace = cloudspace
        machine_name = machine_name

        self.framework.lg('opne %s cloudspace' % cloudspace)
        self.framework.CloudSpaces.open_cloudspace_page(cloudspace)

        self.framework.lg('open %s virtual machine' % machine_name)
        self.framework.set_text('virtual machine search', machine_name)
        self.framework.wait_until_element_located_and_has_text("virtual_machine_table_first_element",
                                                               machine_name)
        vm_id = self.framework.get_text("virtual_machine_table_first_element_2")[3:]
        self.framework.click('virtual_machine_table_first_element')
        self.framework.element_in_url(vm_id)

    def delete_virtual_machine(self, cloudspace='', machine_name=''):
        cloudspace = cloudspace
        machine_name = machine_name

        self.framework.lg('open %s virtual machine' % machine_name)
        self.open_virtual_machine_page(cloudspace, machine_name)

        self.framework.lg('delete the machine')
        self.framework.click('virtual_machine_action')
        self.framework.click('virtual_machine_delete')
        self.framework.set_text('virtual_machine_delete_reason', "Test")
        self.framework.click("virtual_machine_delete_confirm")
        self.framework.wait_until_element_attribute_has_text('delete_vm_dialog', 'style', 'display: none;')
        self.framework.get_page(self.framework.driver.current_url)

        for temp in range(10):
            if self.framework.wait_until_element_located_and_has_text("virtual_machine_page_status", "DESTROYED"):
                return True
            else:
                self.framework.get_page(self.framework.driver.current_url)
        else:
            self.framework.fail("Can't delete this '%s' vm")
