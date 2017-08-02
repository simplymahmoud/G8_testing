import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class VirtualMachinesTest(Framework):

    def setUp(self):
        super(VirtualMachinesTest, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)

    def test01_vm_page_paging_table(self):
        """ PRTL-042
        *Test case to make sure that paging and sorting of vms page are working as expected*

        **Test Scenario:**
        #. go to vms page.
        #. get number of vms
        #. try paging from the available page numbers and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.VirtualMachines.get_it()
        self.assertTrue(self.VirtualMachines.is_at())

        vms_paging_options = [25, 50, 100, 10]
        vms_info = self.Tables.get_table_info('table cloudbroker vmachine info')
        vms_number_max_number = int(vms_info[(vms_info.index('f') + 2):(vms_info.index('entries') - 1)].replace(',', ''))

        for vms_paging_option in vms_paging_options:
            self.select('account selector', vms_paging_option)
            time.sleep(5)
            vms_info_ = self.Tables.get_table_info('table cloudbroker vmachine info')
            vms_number_max_number_ = int(vms_info_[vms_info_.index('f') + 2:vms_info_.index('en') - 1].replace(',', ''))
            vms_avaliable_ = int(vms_info_[(vms_info_.index('to') + 3):(vms_info_.index('of') - 1)].replace(',', ''))
            self.assertEqual(vms_number_max_number, vms_number_max_number_)
            if vms_number_max_number > vms_paging_option:
                self.assertEqual(vms_avaliable_, vms_paging_option)
            else:
                self.assertLess(vms_avaliable_, vms_paging_option)

    def test02_vms_page_table_paging_buttons(self):
        """ PRTL-040
        *Test case to make sure that paging and sorting of vms page are working as expected*

        **Test Scenario:**
        #. go to vms page.
        #. get number of vms.
        #. try paging from start/previous/next/last and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)
        self.VirtualMachines.get_it()
        self.assertTrue(self.VirtualMachines.is_at())

        vms_max_number = self.Tables.get_table_max_number('table cloudbroker vmachine info')
        pagination = self.get_list_items('pagination')

        for _ in range((len(pagination) - 3)):
            vms_start_number = self.Tables.get_table_start_number('table cloudbroker vmachine info')
            vms_end_number = self.Tables.get_table_end_number('table cloudbroker vmachine info')
            previous_button, next_button = self.Tables.get_previous_next_button()

            next_button.click()
            time.sleep(3)

            vms_start_number_ = self.Tables.get_table_start_number('table cloudbroker vmachine info')
            vms_end_number_ = self.Tables.get_table_end_number('table cloudbroker vmachine info')

            self.assertEqual(vms_start_number_, vms_start_number + 10)
            if vms_end_number_ < vms_max_number:
                self.assertEqual(vms_end_number_, vms_end_number + 10)
            else:
                self.assertEqual(vms_end_number_, vms_max_number)

    #@unittest.skip('https://github.com/0-complexity/openvcloud/issues/554')
    def test03_vms_page_table_sorting(self):
        """ PRTL-041
        *Test case to make sure that paging and sorting of vms page are working as expected*

        **Test Scenario:**
        #. go to vms page.
        #. get number of vms
        #. sorting of all fields of vms table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.VirtualMachines.get_it()
        self.assertTrue(self.VirtualMachines.is_at())
        table_head_elements = self.get_table_head_elements('table cloudbroker vmachine')
        self.assertNotEqual(table_head_elements, False)

        for column, element in enumerate(table_head_elements):
            current_column = element.text
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.Tables.get_table_data('table cloudbroker vmachine info')
            self.assertTrue(table_before, 'Error while getting table data before sorting')
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.Tables.get_table_data('table cloudbroker vmachine info')
            self.assertTrue(table_after, 'Error while getting table data after sorting')
            self.assertEqual(len(table_before), len(table_after),
                             'The length of vms table is changing according to sorting by %s' % current_column)
            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column], table_after[(len(table_after) - temp - 1)][column])
            self.lg('pass %s column' % current_column)
