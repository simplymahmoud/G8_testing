from functional_testing.Itsyouonline.api_testing.utils import BaseTest


class JWTBasicTests(BaseTest):

    def setUp(self):
        super(JWTBasicTests, self).setUp()
        self.response = self.Client.jwt.GetScope(self.user)
