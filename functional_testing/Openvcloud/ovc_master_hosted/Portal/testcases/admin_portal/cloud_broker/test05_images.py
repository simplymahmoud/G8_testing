import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from random import randint


class ImagesTests(Framework):
    def setUp(self):
        super(ImagesTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)

    def test01_image_page_paging_table(self):
        """ PRTL-041
        *Test case to make sure that paging and sorting of image  page are working as expected*

        **Test Scenario:**cd
        #. go to Images page.
        #. get number of images
        #. try paging from the available page numbers and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('1- go to Images page')
        self.Images.get_it()
        result = self.Images.is_at()
        self.assertTrue(result)
        image_paging_options = [25, 50, 100, 10]
        self.lg('2- get number of images')

        image_info = self.Tables.get_table_info('table cloudbroker image info')
        image_number_max_number = int(image_info[(image_info.index('f') + 2):(image_info.index('entries') - 1)].replace(',', ''))

        self.lg('3- try paging from the available page numbers and verify it should succeed ')

        for image_paging_option in image_paging_options:
            self.select('account selector', image_paging_option)
            time.sleep(2)
            image_info_ = self.Tables.get_table_info('table cloudbroker image info')
            image_number_max_number_ = int(image_info_[image_info_.index('f') + 2:image_info_.index('en') - 1].replace(',', ''))
            image_avaliable_ = int(image_info_[(image_info_.index('to') + 3):(image_info_.index('of') - 1)].replace(',', ''))
            self.assertEqual(image_number_max_number, image_number_max_number_)
            if image_number_max_number > image_paging_option:
                self.assertEqual(image_avaliable_, image_paging_option)
            else:
                self.assertLess(image_avaliable_, image_paging_option)

    def test02_image_page_table_sorting(self):
        """ PRTL-042
        *Test case to make sure that paging and sorting of images page are working as expected*

        **Test Scenario:**
        #. go to image page.
        #. get all table head elements
        #. sorting of all fields of images table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('- go to image bage')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.lg('- get all table head elements')

        table_head_elements = self.get_table_head_elements('table cloudbroker image')
        self.assertNotEqual(table_head_elements, False)
        self.lg('- sorting of all fields of images table, should be working as expected')
        column_value =0
        for element in table_head_elements:
            current_column = element.text
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.Tables.get_table_data('table cloudbroker image info')
            self.assertTrue(table_before, 'Error while getting table data before sorting')
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.Tables.get_table_data('table cloudbroker image info')
            self.assertTrue(table_after, 'Error while getting table data after sorting')
            self.assertEqual(len(table_before), len(table_after),
                             'The length of account table is changing according to sorting by ID')
            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column_value], table_after[(len(table_after) - temp - 1)][column_value])
            column_value = column_value + 1
            self.lg('pass %s column' % current_column)

    def test03_image_page_table_paging_buttons(self):
        """ PRTL-043
        *Test case to make sure that paging and sorting of images page are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. get number of images
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())

        image_max_number = self.Tables.get_table_max_number('table cloudbroker image info')
        pagination = self.get_list_items('pagination')
        for _ in range((len(pagination) - 3)):
            image_start_number = self.Tables.get_table_start_number('table cloudbroker image info')
            image_end_number = self.Tables.get_table_end_number('table cloudbroker image info')
            previous_button, next_button = self.Tables.get_previous_next_button()
            next_button.click()
            time.sleep(3)

            image_start_number_ = self.Tables.get_table_start_number('table cloudbroker image info')
            image_end_number_ = self.Tables.get_table_end_number('table cloudbroker image info')
            self.assertEqual(image_start_number_, image_start_number + 10)
            if image_end_number_ < image_max_number:
                self.assertEqual(image_end_number_, image_end_number + 10)
            else:
                self.assertEqual(image_end_number_, image_max_number)

    def test04_image_page_searchbox(self):
        """ PRTL-044
        *Test case to make sure that search boxes of images page are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value
        """
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        table_head_elements = self.get_table_head_elements('table cloudbroker image')
        table_before = self.Tables.get_table_data('table cloudbroker image info')
        columns = len(table_head_elements)
        rows= len(table_before)
        random_elemn= randint(0,rows-1)
        self.lg('2-try search of all elements by main search box')
        skip_column =[1, 4]
        for column in range(columns) :
            #skip("bug #https://github.com/0-complexity/openvcloud/issues/696")
            if column in skip_column:
                continue
            self.set_text("image_search", table_before[random_elemn][column])
            time.sleep(2)
            table_after = self.Tables.get_table_data('table cloudbroker image info')
            self.assertTrue(any(table_before[random_elemn][column] in s for s in table_after[0] ))

        self.clear_text("image_search")
        time.sleep(2)


        self.lg('3-try search of all elements by search box in every column')

        for column in range(columns) :
            #skip("bug #https://github.com/0-complexity/openvcloud/issues/696")
            if column in [1,4]:
                continue
            self.assertTrue(self.set_text_columns("image_table_element_search" ,table_before[random_elemn][column], column+1))
            time.sleep(1)
            table_after1=self.Tables.get_table_data('table cloudbroker image info')
            self.assertTrue(table_before[random_elemn][column] in table_after1[0][column])
            self.assertTrue(self.clear_text_columns("image_table_element_search",column+1))


    def test05_stack_table_in_image_page_test(self):
        """ PRTL-045

        **Test Scenario:**

        #. go to images page.
        #. open random image page
        #. get number of stacks
        #. try paging from the available page numbers in stack table  and verify it should succeed
        #. sorting of all fields of virtual machine table, should be working as expected
        #. try paging from start/previous/next/last and verify it should succeed
        """

        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())

        self.lg('2- open random image page')

        table_elements=self.Tables.get_table_data('table cloudbroker image info')
        rows= len(table_elements)
        random_elemn= randint(0,rows-1)
        image_element=table_elements[random_elemn][0]
        self.Images.open_image_page(image_element)
        time.sleep(2)
        self.lg('stacks which have this Image table ')
        paging_options = [25, 50, 100, 10]

        self.lg('3- get number of stacks')

        stacks_info = self.Tables.get_table_info('table cloudbroker stack info')
        stacks_number_max_number = int(stacks_info[(stacks_info.index('f') + 2):(stacks_info.index('entries') - 1)].replace(',', ''))

        self.lg('4- try paging from the available page numbers and verify it should succeed ')

        for paging_option in paging_options:
            self.select('account selector', paging_option)
            time.sleep(1)
            stack_info_ = self.Tables.get_table_info('table cloudbroker stack info')
            stack_number_max_number_ = int(stack_info_[stack_info_.index('f') + 2:stack_info_.index('en') - 1].replace(',', ''))
            stack_avaliable_ = int(stack_info_[(stack_info_.index('to') + 3):(stack_info_.index('of') - 1)].replace(',', ''))
            self.assertEqual(stacks_number_max_number, stack_number_max_number_)
            if stacks_number_max_number > paging_option:
                self.assertEqual(stack_avaliable_, paging_option)
            else:
                self.assertLess(stack_avaliable_, paging_option)

        self.lg('- get all table head elements')
        table_head_elements = self.get_table_head_elements('table cloudbroker stack')
        self.assertNotEqual(table_head_elements, False)
        self.lg('5- sorting of all fields of images table, should be working as expected')
        column_value =0
        for element in table_head_elements:
            current_column = element.text
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.Tables.get_table_data('table cloudbroker stack info', pagination='stack_table_pagination')
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.Tables.get_table_data('table cloudbroker stack info', pagination='stack_table_pagination')
            self.assertEqual(len(table_before), len(table_after),
                             'The length of image table is changing according to sorting by %s'%current_column)
            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column_value], table_after[(len(table_after) - temp - 1)][column_value])
            column_value = column_value + 1
            self.lg('pass %s column' % current_column)

        self.lg('6-try paging from start/previous/next/last and verify it should succeed')

        stacks_max_number = self.Tables.get_table_max_number('table cloudbroker stack info')
        pagination = self.get_list_items('pagination')
        for _ in range((len(pagination) - 3)):
            stack_start_number = self.Tables.get_table_start_number('table cloudbroker stack info')
            stack_end_number = self.Tables.get_table_end_number('table cloudbroker stack info')
            previous_button, next_button = self.Tables.get_previous_next_button()
            next_button.click()
            time.sleep(3)
            stack_end_number_ = self.Tables.get_table_end_number('table cloudbroker stack info')
            stack_start_number_ = self.Tables.get_table_start_number('table cloudbroker image info')

            self.assertEqual(stack_start_number_, stack_start_number + 10)
            if stack_end_number_ < stack_max_number:
                self.assertEqual(stack_end_number_, stack_end_number + 10)
            else:
                self.assertEqual(stack_end_number_, stack_max_number)


    def test06_VM_table_in_image_page_test(self):
        """ PRTL-046

        **Test Scenario:**

        #. go to images page.
        #. open random image page
        #. get number of vms
        #. try paging from the available page numbers in stack table  and verify it should succeed
        #. sorting of all fields of virtual machine table, should be working as expected
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('1- go to Images page')

        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        table_elements=self.Tables.get_table_data('table cloudbroker image info', pagination='VM_table_pagination')

        self.lg('2- open random Image page')

        rows= len(table_elements)
        random_elemn= randint(0,rows-1)
        image_element=table_elements[random_elemn][0]
        self.Images.open_image_page(image_element)
        time.sleep(2)
        self.lg(' which have this Image table ')
        paging_options = [25, 50, 100, 10]

        self.lg('3- get number of vms')

        VM_info = self.Tables.get_table_info('table cloudbroker vmachine info')
        VM_number_max_number = int(VM_info[(VM_info.index('f') + 2):(VM_info.index('entries') - 1)].replace(',', ''))
        self.lg('number of vms %s'% VM_number_max_number)

        self.lg('4- try paging from the available page numbers and verify it should succeed ')

        for paging_option in paging_options:

            self.select('VM_table selector', paging_option)
            time.sleep(4)
            VM_info_ = self.Tables.get_table_info('table cloudbroker vmachine info')
            VM_number_max_number_ = int(VM_info_[VM_info_.index('f') + 2:VM_info_.index('en') - 1].replace(',', ''))
            VM_avaliable_ = int(VM_info_[(VM_info_.index('to') + 3):(VM_info_.index('of') - 1)].replace(',', ''))
            self.assertEqual(VM_number_max_number, VM_number_max_number_)
            if VM_number_max_number > paging_option:
                self.assertEqual(VM_avaliable_, paging_option)
            else:
                self.assertLess(VM_avaliable_, paging_option)

        self.lg('- get all table head elements')
        table_head_elements = self.get_table_head_elements('table cloudbroker vmachine')
        self.assertNotEqual(table_head_elements, False)
        self.lg('5- sorting of all fields of virtual machine table, should be working as expected')

        column_value =0
        for element in table_head_elements:
            current_column = element.text
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.Tables.get_table_data('table cloudbroker vmachine info','VM_table selector','table cloudbroker vmachine','VM_table_pagination')
            self.assertNotEqual(table_before,False,'Error while getting table data befor sorting')
            self.driver.execute_script("window.scrollTo(0, 0)")
            element.click()
            self.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.Tables.get_table_data('table cloudbroker vmachine info','VM_table selector','table cloudbroker vmachine','VM_table_pagination')
            self.assertNotEqual(table_after,False, 'Error while getting table data after sorting')
            self.assertEqual(len(table_before), len(table_after),
                             'The length of image table is changing according to sorting by %s'%current_column)
            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column_value], table_after[(len(table_after) - temp - 1)][column_value])
            column_value = column_value + 1
            self.lg('pass %s column' % current_column)

        self.lg('6- try paging from start/previous/next/last and verify it should succeed')
        VM_max_number = self.Tables.get_table_max_number('table cloudbroker vmachine info')
        pagination = self.get_list_items('pagination')
        for _ in range((len(pagination) - 3)):
            VM_start_number = self.Tables.get_table_start_number('table cloudbroker vmachine info')
            VM_end_number = self.Tables.get_table_end_number('table cloudbroker vmachine info')
            previous_button, next_button = self.Tables.get_previous_next_button()
            next_button.click()
            time.sleep(3)
            VM_end_number_ = self.Tables.get_table_end_number('table cloudbroker vmachine info')
            VM_start_number_ = self.Tables.get_table_start_number('table cloudbroker vmachine info')
            self.assertEqual(VM_start_number_, VM_start_number + 10)
            if VM_end_number_ < VM_max_number:
                self.assertEqual(VM_end_number_, VM_end_number + 10)
            else:
                self.assertEqual(VM_end_number_, VM_max_number)

    def test07_search_boxes_in_image_page_test(self):
        """ PRTL-047
        *Test case to make sure that search boxes of images page are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. open one random  image page
        #. try use general search box  to search for values in  all columns and verfiy it return the right value in stack table
        #. try use the search box in every column and  verfiy it return the right value in stack table
        #. try use general search box  to search for values in  all columns and verfiy it return the right value in VM table
        #. try use the search box in every column and  verfiy it return the right value in VM table
        """
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())

        self.lg('2-open one random image page')

        table_elements=self.Tables.get_table_data('table cloudbroker image info')
        rows= len(table_elements)
        random_elemn= randint(0,rows-1)
        image_element=table_elements[random_elemn][0]
        self.Images.open_image_page(image_element)
        self.lg('-try search boxes in stack table')

        table_head_elements = self.get_table_head_elements('table cloudbroker stack')
        table_before = self.Tables.get_table_data('table cloudbroker stack info', pagination='stack_table_pagination')
        columns = len(table_head_elements)
        rows= len(table_before)
        info_table_befor=self.get_text('table cloudbroker stack info')
        self.lg('3- try search of all elements by main search box')
        if table_before!=[]:
            random_elemn= randint(0,rows-1)
            for column in range(columns) :
                #skip("bug #https://github.com/0-complexity/openvcloud/issues/696")
                if column == 1 :
                        continue

                self.set_text("stack_search", table_before[random_elemn][column])
                time.sleep(2)
                table_after = self.Tables.get_table_data('table cloudbroker stack info', pagination='stack_table_pagination')
                self.assertTrue(any(table_before[random_elemn][column] in s for s in table_after[0] ))

            self.clear_text("stack_search")
            self.assertTrue(self.wait_until_element_located_and_has_text('table cloudbroker stack info', info_table_befor))
            self.lg('4- try search of all elements by search box in every column')

            for column in range(columns) :
                #skip("bug #https://github.com/0-complexity/openvcloud/issues/696")
                if column == 4 :
                    continue
                self.assertTrue(self.set_text_columns("stack_table_element_search" ,table_before[random_elemn][column], column+1 ))
                table_after1=self.Tables.get_table_data('table cloudbroker stack info', pagination='stack_table_pagination')
                self.assertFalse( 'No data available in table' in table_after1[0] )
                self.assertTrue(table_before[random_elemn][column] in table_after1[0][column])
                self.assertTrue(self.clear_text_columns("stack_table_element_search",column+1))

        self.lg('-try search boxes in VM table')

        table_head_elements_VM = self.get_table_head_elements('table cloudbroker vmachine')
        self.assertNotEqual(table_head_elements_VM, False)
        table_before_VM = self.Tables.get_table_data('table cloudbroker vmachine info','VM_table selector','table cloudbroker vmachine', pagination='VM_table_pagination')
        time.sleep(2)
        self.lg('5- try search of all elements in vm table by main search box')
        if table_before_VM != [] :
            self.assertTrue(table_before_VM , 'Error while getting table data before searching')
            columns = len(table_head_elements_VM)
            rows= len(table_before_VM)
            random_elemn= randint(0,rows-1)
            info_table_befor=self.get_text('table cloudbroker vmachine info')
            for column in range(columns) :
                #skip("bug #https://github.com/0-complexity/openvcloud/issues/696")
                if column == 3 :
                    continue
                self.set_text("VM_search", table_before_VM[random_elemn][column])
                time.sleep(2)
                table_after = self.Tables.get_table_data('table cloudbroker vmachine info','VM_table selector','table cloudbroker vmachine', pagination='VM_table_pagination')
                self.assertTrue(table_after, 'Error while getting table data after searching')
                self.assertTrue(any(table_before_VM[random_elemn][column] in s for s in table_after[0] ))
            self.clear_text("VM_search")
            self.assertTrue(self.wait_until_element_located_and_has_text('table cloudbroker vmachine info', info_table_befor))
            self.lg('4- try search of all elements by search box in every column')

            for column in range(columns) :
                self.set_text_columns("VM_table_element_search" ,table_before_VM[random_elemn][column], column+1 )
                table_after1=self.Tables.get_table_data('table cloudbroker vmachine info','VM_table selector','table cloudbroker vmachine', pagination='VM_table_pagination')
                self.assertTrue(table_before_VM[random_elemn][column] in table_after1[0][column])
                self.clear_text_columns("VM_table_element_search",column+1)
