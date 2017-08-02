import time
import unittest
import uuid
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework

class Write(Framework):
    def __init__(self, *args, **kwargs):
        super(Write, self).__init__(*args, **kwargs)

    def setUp(self):
        super(Write, self).setUp()
        self.Login.Login()

    def test(self):
        self.assertTrue(self.EUMachines.end_user_create_virtual_machine(machine_name=self.machine_name))
        time.sleep(10)
        print(self.driver.find_element_by_xpath(".//*[@id='actions']/div/div[1]/ul/li[3]/div/div[2]").text)
