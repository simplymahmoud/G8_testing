import time
from random import randint

class tables():
    def __init__(self, framework):
        self.framework = framework

    def get_table_info(self, element):
        for _ in range(10):
            account_info = self.framework.get_text(element)
            if "Showing" in account_info:
                return account_info
            else:
                time.sleep(1)
        else:
            self.framework.fail("Can't get the table info")

    def get_table_start_number(self, table_info_element):
        account_info = self.get_table_info(table_info_element)
        return int(account_info[(account_info.index('g') + 2):(account_info.index('to') - 1)])

    def get_table_end_number(self, table_info_element):
        account_info = self.get_table_info(table_info_element)
        return int(account_info[(account_info.index('to') + 3):(account_info.index('of') - 1)])

    def get_table_max_number(self, table_info_element):
        account_info = self.get_table_info(table_info_element)
        return int(account_info[(account_info.index('f') + 2):(account_info.index('entries') - 1)].replace(',',''))

    def get_previous_next_button(self, element=None):
        if element == None:
            pagination = self.framework.get_list_items('pagination')
        else:
            table = self.framework.find_element(element)
            pagination = table.find_element_by_tag_name('ul')
            pagination = pagination.find_elements_by_tag_name('li')

        previous_button = pagination[0].find_element_by_tag_name('a')
        next_button = pagination[(len(pagination) - 1)].find_element_by_tag_name('a')

        return previous_button, next_button

    def get_table_data(self, element, selector = 'account selector',table_element=None, pagination=None):
        # This method will return a table data as a list
        self.framework.assertTrue(self.framework.check_element_is_exist(element))
        max_sort_value = 100
        account_max_number = self.get_table_max_number(element)
        self.framework.select( selector , max_sort_value)
        time.sleep(6)
        page_numbers = (account_max_number / max_sort_value)
        if (account_max_number % max_sort_value) > 0:
            page_numbers += 1
        tableData = []
        for page in range(page_numbers):

            table_rows = self.framework.get_table_rows(table_element)
            self.framework.assertTrue(table_rows)
            for row in table_rows:
                cells = row.find_elements_by_tag_name('td')
                tableData.append([x.text for x in cells])
            if  page < (page_numbers-1):
                previous_button, next_button = self.get_previous_next_button(pagination)
                next_button.click()

                tb_max_number = self.get_table_max_number(element)
                tb_start_number = 1+((page+1)*max_sort_value)
                tb_end_number = (page+2)*max_sort_value

                if tb_end_number > tb_max_number:
                    tb_end_number = tb_max_number
                text = "Showing %s to %s of %s entries" %("{:,}".format(tb_start_number), "{:,}".format(tb_end_number), "{:,}".format(tb_max_number))
                if not self.framework.wait_until_element_located_and_has_text(element, text):
                    self.framework.lg('table max number changed %s -> %s ' % (account_max_number ,tb_max_number))
                    return False
        return tableData

    def check_show_list(self, info_table, selector):
        paging_options = [25, 50, 100, 10]
        rows_max_number = self.get_table_max_number(info_table)

        for option in paging_options:
            self.framework.select(selector, option)
            time.sleep(3)
            rows_max_number_ = self.get_table_max_number(info_table)
            rows_end_number_ = self.get_table_end_number(info_table)

            if rows_max_number != rows_max_number_:
                return False

            if rows_max_number > option:
                if rows_end_number_ != option:
                    return False
            else:
                if not rows_end_number_ < option:
                    return False

        return True

    def check_next_previous_buttons(self, info_table, pagination=None):
        rows_max_number = self.get_table_max_number(info_table)
        if pagination == None:
            pagination_items = self.framework.get_list_items('pagination')
        else:
            table = self.framework.find_element(pagination)
            pagination_items = table.find_element_by_tag_name('ul')
            pagination_items = pagination.find_elements_by_tag_name('li')

        for _ in range((len(pagination_items) - 3)):
            page_start_number = self.get_table_start_number(info_table)
            page_end_number = self.get_table_end_number(info_table)
            previous_button, next_button = self.get_previous_next_button(pagination)
            next_button.click()
            time.sleep(4)
            page_start_number_ = self.get_table_start_number(info_table)
            page_end_number_ = self.get_table_end_number(info_table)

            if page_start_number_ != page_start_number+10:
                return False
            if page_end_number_ < rows_max_number:
                if page_end_number_ != page_end_number+10:
                    return False
            else:
                if page_end_number_ != rows_max_number:
                    return False

            previous_button, next_button = self.get_previous_next_button(pagination)
            previous_button.click()
            time.sleep(4)
            page_start_number__ = self.get_table_start_number(info_table)
            page_end_number__ = self.get_table_end_number(info_table)

            if page_start_number__ != page_start_number_-10:
                return False

            previous_button, next_button = self.get_previous_next_button(pagination)
            next_button.click()
            time.sleep(4)

        return True

    def check_sorting_table(self, data_table, info_table, selector, pagination=None):
        self.framework.select(selector , 100)
        table_location = self.framework.find_element(data_table).location
        table_head_elements = self.framework.get_table_head_elements(data_table)
        for column, element in enumerate(table_head_elements):
            if 'sorting_disabled' in element.get_attribute('class'):
                continue

            current_column = element.text
            self.framework.driver.execute_script("window.scrollTo(0,%d)" % (table_location['y']-50))
            element.click()
            self.framework.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.get_table_data(info_table, table_element=data_table, pagination=pagination)

            if not table_before:
                return False

            self.framework.driver.execute_script("window.scrollTo(0,%d)" % (table_location['y']-50))
            element.click()
            self.framework.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.get_table_data(info_table, table_element=data_table, pagination=pagination)

            if not table_after:
                return False

            for temp in range(len(table_before)):
                if not table_before[temp][column] == table_after[(len(table_after)-temp-1)][column]:
                    return False

            self.framework.lg('coulmn %s passed' % current_column)

        return True

    def check_search_box(self, data_table, info_table, search_box):
        table_head_elements = self.framework.get_table_head_elements(data_table)
        table_before = self.get_table_data(info_table)
        columns = len(table_head_elements)
        rows = len(table_before)
        random_element = randint(0,rows-1)
        for column in range(columns):
            self.framework.set_text(search_box, table_before[random_element][column])
            time.sleep(2)
            table_after = self.get_table_data(info_table)

            if not any(table_before[random_element][column] in s for s in table_after[0]):
                return False

        self.framework.clear_text(search_box)
        return True

    def check_data_filters(self, data_table, info_table):
        table_before = self.get_table_data(info_table)
        table_head_elements = self.framework.get_table_head_elements(data_table)
        columns = len(table_head_elements)
        rows = len(table_before)
        random_element = randint(0,rows-1)

        table = self.framework.find_element(data_table)
        footer = table.find_element_by_tag_name('tfoot')
        items = footer.find_elements_by_tag_name('td')
        filters = [x.find_elements_by_tag_name('input')[0] for x in items]

        for column in range(columns):
            if 'nofilter' in table_head_elements[column].get_attribute('class'):
                continue

            current_filter = filters[column]
            current_filter.send_keys(table_before[random_element][column])
            time.sleep(1)
            table_after = self.get_table_data(info_table)

            if not table_after[0][column] == table_before[random_element][column]:
                return False

            self.framework.clear_element_text(current_filter)

        return True
