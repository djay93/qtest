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

        if self.is_element_present(LOC.PRODUCT.PRICE_LINE, item):
            priceline = item.find_element(*LOC.PRODUCT.PRICE_LINE)
            qty_list = [ qty.text for qty in priceline.find_elements(*LOC.PRODUCT.DISCOUNT_QTY)]
            amt_list = [amt.text for amt in priceline.find_elements(*LOC.PRODUCT.DISCOUNT_AMT)]

            for i, qty in enumerate(qty_list):
                a,b = qty.replace('+','-').split('-')
                if self.get_number(b) > 10:
                    continue
                elif self.get_number(a) > 10:
                    continue

        product_dict["unit_price"] = item.find_element(*LOC.PRODUCT.PRICE).text

        #click on add to cart button
        self.find_element(LOC.PRODUCT.ADD_TO_CART).click()
        self.wait()

        #shopping cart verification
        cart = self.find_element_and_wait(LOC.CART.CART)
        for cart_item in cart.find_elements(*LOC.CART.CART_ITEM):
            if cart_item.get_attribute("class") == 'header': continue

            #self.verify_regexp_matches(cart_item.find_element(*LOC.CART.UNIT_PRICE), product_dict["unit_price"] )
            product_dict["unit_price"] = cart_item.find_element(*LOC.CART.UNIT_PRICE).text
            self.verify_regexp_matches(cart_item.find_element(*LOC.CART.TITLE), product_dict["title"])
            self.verify_regexp_matches(cart_item.find_element(*LOC.CART.SKU), product_dict["sku"] )
            self.verify_regexp_matches(cart_item.find_element(*LOC.CART.QTY_BOX).get_attribute("value"), "10")

        product_dict["sub_total"] = self.find_element(LOC.CART.SUBTOTAL_VALUE).text
        #click next to go to checkout page
        self.find_element(LOC.CART.CHECKOUT).click()
        self.wait()

        #checkout page verifications
        s_address = self.find_element_and_wait(LOC.CHECKOUT.SHIPPING_ADDRESS)
        address = self.load_data("checkout.address.json")["ny_address"]
        self.checkout_fill_address(s_address, address)
        self.wait()
        city = s_address.find_element(*LOC.CHECKOUT.CITY)
        self.verify_value_equal(city.get_attribute("value"), address["city"])
        state = s_address.find_element(*LOC.CHECKOUT.STATE)
        self.verify_value_equal(state, address["state"])

        #select shipping type
        s_options = self.find_element_and_wait(LOC.CHECKOUT.SHIPPING_OPTION_LIST)
        li = s_options.find_elements_by_css_selector("ul li")
        id = randrange(0, len(li) - 1)
        li[id].find_element_by_css_selector("input").click()
        #li[id].find_element_by_css_selector("div span.shipping-method")

        #fill the payment details
        payment_details = self.find_element_and_wait(LOC.CHECKOUT.PAYMENT_DETAILS)
        payment = self.load_data("checkout.payment.json")["visa.match"]
        self.checkout_fill_payment_details(payment)

        #verify & store attributes
        order_nav = self.find_element(LOC.CHECKOUT.ORDER_NAV)
        sub_total = order_nav.find_element(*LOC.CHECKOUT.SUBTOTAL_VALUE)
        self.verify_value_equal(sub_total, product_dict["sub_total"])
        product_dict["tax_value"] = order_nav.find_element(*LOC.CHECKOUT.TAX_VALUE).text
        shipping_value = order_nav.find_element(*LOC.CHECKOUT.SHIPPING_VALUE).text
        if '$' in shipping_value:
            product_dict["shipping_value"] = '$' + shipping_value.split('$')[1]
        else:
            product_dict["shipping_value"] = "$0.00"
        product_dict["order_total"] = order_nav.find_element(*LOC.CHECKOUT.ORDER_TOTAL).text

        #click on place your order button
        self.find_element(LOC.CHECKOUT.PLACE_ORDER).click()
        self.wait()
        order_totals = self.find_element_and_wait(LOC.CHECKOUT_RECEIPT.ORDER_TOTALS)
        sub_total = order_totals.find_element(*LOC.CHECKOUT_RECEIPT.SUB_TOTAL_VALUE)
        self.verify_value_equal(sub_total, product_dict["sub_total"])
        tax_value = order_totals.find_element(*LOC.CHECKOUT_RECEIPT.TAX_VALUE)
        self.verify_value_equal(tax_value, product_dict["tax_value"])
        shipping_value = order_totals.find_element(*LOC.CHECKOUT_RECEIPT.SHIPPING_VALUE)
        #self.verify_value_equal(shipping_value, product_dict["shipping_value"])
        total_value = order_totals.find_element(*LOC.CHECKOUT_RECEIPT.TOTAL_VALUE)
        #self.verify_value_equal(total_value, product_dict["order_total"])

