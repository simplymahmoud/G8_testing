import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class StorageRoutersTests(Framework):

    def setUp(self):
        super(StorageRoutersTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)
        self.table_info = 'table storagerouter info'
        self.data_table = 'table storagerouter'
        self.selector   = 'table storagerouter length'
        self.search_box = 'storagerouter search'
        self.navigation_bar = 'navigation bar'


    def test01_storagerrouters_page_basic_elements(self):
        """
        PRTL-001
        *Test case to make sure the basic elements in storage routers page as expected*

        **Test Scenario:**
        #. go to storage routers page
        #. check page url & title
        #. check navigation bar
        #. check page title
        #. check 'show records per page' list
        """
        self.lg('go to storage routers page')
        self.StorageRouters.get_it()
        self.assertTrue(self.StorageRouters.is_at())

        self.lg('check page url & title')
        self.assertEqual(self.driver.title, 'CBGrid - Storage Routers')
        self.assertIn('cbgrid/Storage%20Routers', self.driver.current_url)

        self.lg('check navigation bar')
        self.assertEqual(self.get_navigation_bar(self.navigation_bar), ['Cloud Broker','Storage Routers'])

        self.lg('check page title')
        self.assertEqual(self.get_text('page title'), 'Storage Routers')

        self.lg('check "show records per page" list')
        self.assertTrue(self.element_is_enabled(self.selector))

    def test02_storagerrouters_page_paging_table(self):
        """
        PRTL-002
        *Test case to make sure that show 'records per page' of storage routers page is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try paging from the available page numbers and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('go to storage routers page')
        self.StorageRouters.get_it()
        self.assertTrue(self.StorageRouters.is_at())

        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_show_list(self.table_info, self.selector))

        self.lg('%s ENDED' % self._testID)

    def test03_storagerrouters_page_table_paging_buttons(self):
        """
        PRTL-003
        *Test case to make sure that paging of storage routers page is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try paging from start/previous/next/last and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('go to storage routers page')
        self.StorageRouters.get_it()
        self.assertTrue(self.StorageRouters.is_at())

        self.lg('try paging from start/previous/next/last and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons(self.table_info))

        self.lg('%s ENDED' % self._testID)

    def test04_storagerrouters_table_sorting(self):
        """
        PRTL-004
        *Test case to make sure that sorting of storage routers table is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. sorting of all fields of storage routers table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('go to storage routers page')
        self.StorageRouters.get_it()
        self.assertTrue(self.StorageRouters.is_at())

        self.lg('sorting of all fields of storage routers table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table(self.data_table, self.table_info, self.selector))

        self.lg('%s ENDED' % self._testID)

    def test05_storagerrouters_table_search(self):
        """
        PRTL-005
        *Test case to make sure that searching in storage routers table is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try general search box to search for values in all columns and verfiy it return the right value
        #. try the search box in every column and  verfiy it return the right value
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('go to storage routers page')
        self.StorageRouters.get_it()
        self.assertTrue(self.StorageRouters.is_at())

        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box(self.data_table, self.table_info, self.search_box))

        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters(self.data_table, self.table_info))

        self.lg('%s ENDED' % self._testID)
