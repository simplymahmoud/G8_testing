import uuid
from nose_parameterized import parameterized
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from selenium.webdriver.common.by import By

class LoginLogoutPortalTests(Framework):

    def test001_login_and_portal_title(self):
        self.Login.Login()
        self.Logout.End_User_Logout()