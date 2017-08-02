import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class UsersTests(Framework):

    def setUp(self):
        super(UsersTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)

    def test01_users_page_paging_table(self):
        """ PRTL-039
        *Test case to make sure that paging and sorting of users page are working as expected*

        **Test Scenario:**

        #. go to users page.
        #. get number of users
        #. try paging from the available page numbers and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.Users.get_it()
        self.assertTrue(self.Users.is_at())

        users_paging_options = [25, 50, 100, 10]
        users_info = self.Tables.get_table_info('table system user info')
        users_number_max_number = int(users_info[(users_info.index('f') + 2):(users_info.index('entries') - 1)].replace(',',''))

        for users_paging_option in users_paging_options:
            self.select('user selector', users_paging_option)
            time.sleep(5)
            users_info_ = self.Tables.get_table_info('table system user info')
            users_number_max_number_ = int(users_info_[users_info_.index('f') + 2:users_info_.index('en') - 1].replace(',',''))
            users_avaliable_ = int(users_info_[(users_info_.index('to') + 3):(users_info_.index('of') - 1)].replace(',',''))
            self.assertEqual(users_number_max_number, users_number_max_number_)
            if users_number_max_number > users_paging_option:
                self.assertEqual(users_avaliable_, users_paging_option)
            else:
                self.assertLess(users_avaliable_, users_paging_option)

    def test02_users_page_table_paging_buttons(self):
        """ PRTL-040
        *Test case to make sure that paging and sorting of users page are working as expected*

        **Test Scenario:**

        #. go to users page.
        #. get number of users.
        #. try paging from start/previous/next/last and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)
        self.Users.get_it()
        self.assertTrue(self.Users.is_at())

        users_max_number = self.Tables.get_table_max_number('table system user info')
        pagination = self.get_list_items('pagination')

        for _ in range((len(pagination) - 3)):
            users_start_number = self.Tables.get_table_start_number('table system user info')
            users_end_number = self.Tables.get_table_end_number('table system user info')
            previous_button, next_button = self.Tables.get_previous_next_button()

            next_button.click()
            time.sleep(3)

            users_start_number_ = self.Tables.get_table_start_number('table system user info')
            users_end_number_ = self.Tables.get_table_end_number('table system user info')

            self.assertEqual(users_start_number_, users_start_number + 10)
            if users_end_number_ < users_max_number:
                self.assertEqual(users_end_number_, users_end_number + 10)
            else:
                self.assertEqual(users_end_number_, users_max_number)

    #@unittest.skip('https://github.com/0-complexity/openvcloud/issues/554')
    def test03_users_page_table_sorting(self):
        """ PRTL-041
        *Test case to make sure that paging and sorting of users page are working as expected*

        **Test Scenario:**

        #. go to users page.
        #. get number of users
        #. sorting of all fields of users table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.Users.get_it()
        self.assertTrue(self.Users.is_at())

        table_head_elements = self.get_table_head_elements('table system user')
        self.assertNotEqual(table_head_elements, False)

        for column, element in enumerate(table_head_elements):
            current_column = element.text
            if current_column == 'Groups':
                continue

            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.Tables.get_table_data('table system user info', selector='user selector')
            self.assertTrue(table_before, 'Error while getting table data before sorting')
            self.driver.execute_script("window.scrollTo(0, 0)");
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.Tables.get_table_data('table system user info', selector='user selector')
            self.assertTrue(table_after, 'Error while getting table data after sorting')
            self.assertEqual(len(table_before), len(table_after),
                             'The length of users table is changing according to sorting by %s' % current_column)
            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column], table_after[(len(table_after) - temp - 1)][column])
            self.lg('pass %s column' % current_column)
