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

        #verify elements in the left side of product overview
        main = self.find_element_and_wait(LOC.PRODUCT.MAIN)
        left = main.find_element(*LOC.PRODUCT.LEFT)

        title = left.find_element(*LOC.PRODUCT.TITLE)
        product_dict["title"] = title.text
        self.verify_regexp_matches(title, 'Norton 1600')

        desc = left.find_element(*LOC.PRODUCT.DESCRIPTION)
        self.verify_eval_true(desc.text >  0 )

        sku = left.find_element(*LOC.PRODUCT.SKU)
        product_dict["sku"] = sku.text
        self.verify_eval_true(product_dict["sku"] >  0 )

        #verify kit components
        left.find_element(*LOC.PRODUCT.KIT_COMPONENTS)

        #verify item summary section on the right
        right = main.find_element(*LOC.PRODUCT.RIGHT)
        item = right.find_element(*LOC.PRODUCT.ITEM_SUMMARY)
        availability = item.find_element(*LOC.PRODUCT.AVAILABILITY)
        self.verify_regexp_matches(availability, 'In Stock')
        product_price = item.find_element(*LOC.PRODUCT.PRICE)
        self.verify_regexp_matches( product_price, "^\$?(\d*\.\d{1,2})$")

        #select item options if available
        if self.is_element_present(LOC.PRODUCT.OPTION_DIV, item):
            self.product_select_options()

            options = item.find_elements(*LOC.PRODUCT.OPTION_DIV)
            product_dict["options"] = [option.find_element_by_css_selector("div span").text for option in options]

        #set qty
        self.product_set_quantity("10")

