import time
import uuid
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu


class images():
    def __init__(self, framework):
        self.framework = framework
        self.LeftNavigationMenu = leftNavigationMenu(framework)

    def get_it(self):
        self.LeftNavigationMenu.CloudBroker.Images()

    def is_at(self):
        for _ in range(10):
            if 'Images' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def open_image_page(self, image=''):
        self.LeftNavigationMenu.CloudBroker.Images()
        self.framework.set_text("image_search", image)
        self.framework.wait_until_element_located_and_has_text("image_table_first_element_2",
                                                               image)
        image_herf = self.framework.element_link("image_table_first_element_2")
        image_id = image_herf[image_herf.find('?id=')+len('?id='):]
        self.framework.click("image_table_first_element_2")
        self.framework.element_in_url(image_id )
