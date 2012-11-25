__author__ = 'EpiCenter'

import unittest
import time
import re
import urllib2
import os
from random import randrange

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
from exceptions import *
from testcases import LOC
from pyvirtualdisplay import Display

BROWSER = os.environ.get('SELENIUM_BROWSER', 'internetexplorer')
VERSION = os.environ.get('SELENIUM_BROWSER_VERSION', None)
PLATFORM = os.environ.get('SELENIUM_BROWSER_PLATFORM', None)
RC_HOST = os.environ.get('SELENIUM_RC_HOST', 'http://localhost:4444/wd/hub')
ENV = os.environ.get('SELENIUM_ENV', 'LOCAL')
BASE_URL= os.environ.get('BASE_URL', 'http://beta.qualifiedhardware.com/')
USER_NAME= os.environ.get('USER_NAME', 'rohini')
PASSWORD= os.environ.get('PASSWORD', 'pass123')
DRIVERS = ('firefox', 'chrome', 'safari', 'internetexplorer')
TIMEOUT = float(os.environ.get("REQUESTS_TIMEOUT", 3))

class BaseTestCase(unittest.TestCase):

    def get_driver(self):
        return self.driver

    @classmethod
    def setUpClass(cls):
        cls.display = Display(visible=0, size=(1024, 768))
        cls.display.start()

        if BROWSER.lower() not in DRIVERS:
            raise TypeError("You specified browser which not supported by Selenium: %s" % BROWSER)

        if ENV == 'REMOTE':
            capabilities = getattr(webdriver.DesiredCapabilities, BROWSER.upper())
            if VERSION:
                capabilities.update({'version': VERSION})
            if PLATFORM:
                capabilities.update({'platform': PLATFORM})
            cls.driver = webdriver.Remote(RC_HOST, capabilities)
        else:
            if BROWSER.lower() == 'chrome':
                cls.driver = webdriver.Chrome()
            elif BROWSER.lower() == 'firefox':
                cls.driver = webdriver.Firefox()
            elif BROWSER.lower() == 'internetexplorer':
                cls.driver = webdriver.Ie()
            elif BROWSER.lower() == 'opera':
                cls.driver = webdriver.Opera()
        #implicit wait time
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.display.stop

    @classmethod
    def find_element(cls, element, parent=None):
        browser = cls.driver
        if parent is not None:
            browser = parent
        return browser.find_element(*element)

    @classmethod
    def find_elements(cls, element, parent=None):
        browser = cls.driver
        if parent is not None:
            browser = parent
        return browser.find_elements(*element)

    @classmethod
    def find_element_and_wait(cls, element, parent=None, timeout=30):
        try:
            browser = cls.driver
            if parent is not None:
                browser = parent
            return WebDriverWait(browser, timeout).until(lambda browser: browser.find_element(*element))
        except:
            raise TimeoutException(element=element)

    @classmethod
    def find_elements_and_wait(cls, element, parent=None, timeout=30):
        try:
            browser = cls.driver
            if parent is not None:
                browser = parent
            return WebDriverWait(browser, timeout).until(lambda browser: browser.find_elements(*element))
        except:
            raise TimeoutException(element=element)

    def wait(self):
        """
        Shortcut to wait for N seconds
        """
        time.sleep(TIMEOUT)

    def verify_css_value(self, element, css_prop, css_value, parent=None, message = ""):
        """
        Compares CSS property of a WebElement
        """
        if isinstance(element, WebElement):
            self.assertTrue(self.to_unicode(css_value) in self.to_unicode(element.value_of_css_property(css_prop)), message)
        else:
            self.assertTrue(self.to_unicode(css_value) in self.to_unicode(self.find_element(element, parent).value_of_css_property(css_prop)), message)

        return True

    def verify_attribute_value(self, element, attr, value, parent = None, message = ""):
        """
        Compares attribute value of a WebElement
        """
        if isinstance(element, WebElement):
            self.assertTrue(self.to_unicode(value) in self.to_unicode(element.get_attribute(attr)),message)
        else:
            self.assertTrue(self.to_unicode(value) in self.to_unicode(self.find_element(element, parent).get_attribute(attr)),message)

        return True

    def verify_value_equal(self, element, want, parent=None, message = ""):
        """

        """
        if isinstance(element, WebElement):
            self.assertEqual(self.to_unicode(element.text), self.to_unicode(want),message)
        elif isinstance(element, tuple):
            self.assertEqual(self.to_unicode(self.find_element(element, parent).text), self.to_unicode(want), message)
        else:
            self.assertEqual(self.to_unicode(element), self.to_unicode(want), message)

        return True

    def verify_not_equal(self, element, want, parent=None, message = ""):
        """

        """
        if isinstance(element, WebElement):
            self.assertNotEqual(self.to_unicode(element.text), self.to_unicode(want), message)
        elif 'LOC' in element:
            self.assertNotEqual(self.to_unicode(self.find_element(element, parent).text), self.to_unicode(want), message)
        else:
            self.assertNotEqual(self.to_unicode(element), self.to_unicode(want), message)

        return True

    def verify_eval_true(self, str, message = ""):
        self.assertTrue(str, message)
        return True

    def verify_element_not_present(self, element, parent=None, message = "Element is present"):
        isExists = self.is_element_present(element, parent)
        self.assertFalse(isExists,message)
        return isExists

    def verify_element_present(self, element, parent=None, message = "Element is not present"):
        isExists = self.is_element_present(element, parent)
        self.assertTrue(isExists,message)
        return isExists

    def verify_visible(self, element,parent=None, message = ""):
        """
        Verify if the element is displayed or hidden
        """
        if isinstance(element, WebElement):
            self.assertTrue(element.is_displayed(),message)
        else:
            self.assertTrue(self.find_element(element, parent).is_displayed(),message)
        return True

    def verify_regexp_matches(self, ele, exp, message = ""):
        if isinstance(ele, WebElement):
            self.assertTrue(re.compile(exp).search(self.to_unicode(ele.text)), message)
        else:
            self.assertTrue(re.compile(exp).search(self.to_unicode(ele)), message)
        return True

    def move_slider_by_pixel(self, element, pixel, parent = None):
        ele = self.find_element(element, parent)
        action_chains = ActionChains(self.get_driver())
        action_chains.click_and_hold(ele).move_by_offset(pixel, 0).release(ele).perform()


    def is_element_present(self, ele, parent=None):
        """
        Returns true if the element is present
        """

        isExists = False
        try:
            if self.find_element(ele, parent):
                isExists = True
        except NoSuchElementException:
            isExists = False
        return isExists

    def to_unicode(self, s):
        if isinstance(s, str): return s.decode('unicode-escape')
        return s

    def get_number(self, str):
        """
        Return the float value of the given input string after stripping $ or other non decimal values
        """
        nbr = [c if c in "0123456789." else "" for c in str]

        if not str == "" and len(nbr) > 0:
            return float("".join(nbr))

        return 0

    def contains_in_web_page(self, url, find):
        soup = BeautifulSoup(urllib2.urlopen(url))
        s = soup.find(text = re.compile(find, re.IGNORECASE))

        if self.verify_eval_true(s is not None and len(s) > 0, find + " text not present in href " + url):
            return True
        return False

    def search_product(self, key):
        """
        Searches a product in home page
        """
        search_div = self.find_element(LOC.HEADER.SEARCH_DIV)
        search_div.find_element(*LOC.HEADER.SEARCH_TEXT).send_keys(key)
        search_div.find_element(*LOC.HEADER.SEARCH_BUTTON).click()

    def product_select_options(self):
        """
        This method will select the options for the product
        """
        options = self.find_element(LOC.PRODUCT.ITEM_SUMMARY).find_elements(*LOC.PRODUCT.OPTION_DIV)
        for option in options:
            #pull down the option
            if self.verify_css_value(option.find_element_by_css_selector("ul"), "display", "none"):
                option.find_element_by_css_selector("div a").click()

            #get the items from the list
            li = option.find_elements_by_css_selector("ul li")
            li[randrange(2, len(li) - 1)].find_element_by_xpath("a").click()

    def product_set_quantity(self, qty):
        qty_div = self.find_element(LOC.PRODUCT.ITEM_SUMMARY).find_element(*LOC.PRODUCT.QTY_DIV)
        qty_div.find_element(*LOC.PRODUCT.QTY_BOX).clear()
        qty_div.find_element(*LOC.PRODUCT.QTY_BOX).send_keys(qty)
        qty_div.find_element(*LOC.PRODUCT.QTY_ASC).click()
        qty_div.find_element(*LOC.PRODUCT.QTY_DESC).click()

    def checkout_fill_address(self, element, address):
        element.find_element(*LOC.CHECKOUT.FIRST_NAME).send_keys(address["first_name"])
        element.find_element(*LOC.CHECKOUT.LAST_NAME).send_keys(address["last_name"])
        element.find_element(*LOC.CHECKOUT.COMPANY).send_keys(address["company"])
        element.find_element(*LOC.CHECKOUT.EMAIL).send_keys(address["email"])
        element.find_element(*LOC.CHECKOUT.PHONE).send_keys(address["phone"])
        element.find_element(*LOC.CHECKOUT.ADDRESS).send_keys(address["address"])
        element.find_element(*LOC.CHECKOUT.ADDRESS_2).send_keys(address["address_2"])
        element.find_element(*LOC.CHECKOUT.ZIP_CODE).send_keys(address["zip_code"])

    def checkout_fill_payment_details(self, payment):
        payment_details = self.find_element_and_wait(LOC.CHECKOUT.PAYMENT_DETAILS)
        payment_details.find_element(*LOC.CHECKOUT.CC_NUMBER).send_keys(payment["cc_number"])
        payment_details.find_element(*LOC.CHECKOUT.SECURITY_CODE).send_keys(payment["security_code"])
        #payment_details.find_element(*LOC.CHECKOUT.EXP_MONTH).send_keys(payment["exp_month"])
        #payment_details.find_element(*LOC.CHECKOUT.EXP_YEAR).send_keys(payment["exp_year"])

