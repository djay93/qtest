__author__ = 'EpiCenter'
__testcaseid__='QH-AUTO-001'

import json
from random import randrange
from lib.base import *
from testcases import LOC

class TestNorton1600(BaseTestCase):

    def setUp(self):
        super(TestNorton1600, self).setUp()

        #Open the Qualified Hardware Home page
        self.driver.get(BASE_URL)

    def load_data(self, file):
        data = json.loads(open(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "conf", file)).read())
        return data

    def test_checkout(self):
        product_dict = {}

        #Verify whether QH Header is loaded or not
        self.find_element(LOC.HEADER.HEADER_LOGO)

        #Search Norton 1600 Product
        self.search_product("Norton 1600")
        #self.wait()

