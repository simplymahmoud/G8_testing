import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu


class storagerouters():
    def __init__(self, framework):
        self.framework = framework
        self.LeftNavigationMenu = leftNavigationMenu(framework)

    def get_it(self):
        self.LeftNavigationMenu.CloudBroker.StorageRouters()

    def is_at(self):
        for _ in range(10):
            if 'Storage Routers' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    
