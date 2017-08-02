from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloud_broker.accounts import accounts
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloud_broker.cloudspaces import cloudspaces
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloud_broker.virtualmachines import virtualmachines
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.grid.error_conditions import errorConditions
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.grid.status_overview import statusOverview
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import leftNavigationMenu
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.right_navigation_menu import rightNavigationMenu
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloud_broker.users import users
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.end_user_portal.home import home
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.end_user_portal.machines import machines
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.workflow.login import login
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.workflow.logout import logout
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.workflow.tables import tables
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloud_broker.Images import images
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloud_broker.storagerouters import storagerouters

class Framework(BaseTest):
    def __init__(self, *args, **kwargs):
        super(Framework, self).__init__(*args, **kwargs)

        #Pages.AdminPortal.Cloud_broker
        self.Users = users(self)
        self.Accounts = accounts(self)
        self.CloudSpaces = cloudspaces(self)
        self.VirtualMachines = virtualmachines(self)
        self.Images = images(self)
        self.StorageRouters = storagerouters(self)
        #Pages.AdminPortal.grid
        self.ErrorConditions = errorConditions(self)
        self.StatusOverview = statusOverview(self)

        #pages.end_user
        self.EUHome = home(self)
        self.EUMachines = machines(self)

        #NAvigation
        self.LeftNavigationMenu = leftNavigationMenu(self)
        self.RightNavigationMenu = rightNavigationMenu(self)

        #workflow
        self.Login = login(self)
        self.Logout = logout(self)
        self.Tables = tables(self)
