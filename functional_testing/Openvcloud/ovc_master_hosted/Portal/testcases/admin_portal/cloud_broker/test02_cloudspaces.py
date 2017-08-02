import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class CloudspacesTests(Framework):
    def setUp(self):
        super(CloudspacesTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)

    def test01_cloudspace_page_paging_table(self):
        """ PRTL-033
        *Test case to make sure that paging and sorting of cloudspaces page are working as expected*

        **Test Scenario:**

        #. go to cloudspaces page.
        #. get number of cloudspaces
        #. try paging from the available page numbers and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.CloudSpaces.get_it()
        self.assertTrue(self.CloudSpaces.is_at())

        account_paging_options = [25, 50, 100, 10]
        account_info = self.Tables.get_table_info('table cloudbroker cloudspace info')
        account_number_max_number = int(account_info[(account_info.index('f') + 2):(account_info.index('entries') - 1)].replace(',', ''))

        for account_paging_option in account_paging_options:
            self.select('cloudspace selector', account_paging_option)
            time.sleep(5)
            account_info_ = self.Tables.get_table_info('table cloudbroker cloudspace info')
            account_number_max_number_ = int(account_info_[account_info_.index('f') + 2:account_info_.index('en') - 1].replace(',', ''))
            account_avaliable_ = int(account_info_[(account_info_.index('to') + 3):(account_info_.index('of') - 1)].replace(',', ''))
            self.assertEqual(account_number_max_number, account_number_max_number_)
            if account_number_max_number > account_paging_option:
                self.assertEqual(account_avaliable_, account_paging_option)
            else:
                self.assertLess(account_avaliable_, account_paging_option)

    def test05_cloudspace_page_table_paging_buttons(self):
        """ PRTL-034
        *Test case to make sure that paging and sorting of accounts page are working as expected*

        **Test Scenario:**

        #. go to accounts page.
        #. get number of accounts
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.CloudSpaces.get_it()
        self.assertTrue(self.CloudSpaces.is_at())

        account_max_number = self.Tables.get_table_max_number('table cloudbroker cloudspace info')
        pagination = self.get_list_items('pagination')

        for _ in range((len(pagination) - 3)):
            account_start_number = self.Tables.get_table_start_number('table cloudbroker cloudspace info')
            account_end_number = self.Tables.get_table_end_number('table cloudbroker cloudspace info')
            previous_button, next_button = self.Tables.get_previous_next_button()

            next_button.click()
            time.sleep(3)

            account_start_number_ = self.Tables.get_table_start_number('table cloudbroker cloudspace info')
            account_end_number_ = self.Tables.get_table_end_number('table cloudbroker cloudspace info')

            self.assertEqual(account_start_number_, account_start_number + 10)
            if account_end_number_ < account_max_number:
                self.assertEqual(account_end_number_, account_end_number + 10)
            else:
                self.assertEqual(account_end_number_, account_max_number)

    #@unittest.skip('https://github.com/0-complexity/openvcloud/issues/526')
    def test06_cloudspace_page_table_sorting(self):
        """ PRTL-035
        *Test case to make sure that paging and sorting of accounts page are working as expected*

        **Test Scenario:**

        #. go to accounts page.
        #. get number of accounts
        #. sorting of all fields of accounts table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.CloudSpaces.get_it()
        self.assertTrue(self.CloudSpaces.is_at())
        table_head_elements = self.get_table_head_elements('table cloudbroker cloudspace')
        self.assertNotEqual(table_head_elements, False)

        for column, element in enumerate(table_head_elements):
            current_column = element.text
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.Tables.get_table_data('table cloudbroker cloudspace info', selector='cloudspace selector')
            self.assertTrue(table_before, 'Error while getting table data before sorting')
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.Tables.get_table_data('table cloudbroker cloudspace info', selector='cloudspace selector')
            self.assertTrue(table_after, 'Error while getting table data after sorting')
            self.assertEqual(len(table_before), len(table_after),
                             'The length of account table is changing according to sorting by ID')
            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column], table_after[(len(table_after) - temp - 1)][column])
            self.lg('pass %s column' % current_column)
