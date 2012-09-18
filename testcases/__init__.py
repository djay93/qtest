__author__ = 'EpiCenter'

from selenium.webdriver.common.by import By

class LOC(object):
    class MENU(object):
        HOME = (By.XPATH, "//nav/ul/li[text()='Home']")
        DOCUMENTS = (By.XPATH, "//nav/ul/li[text()='Documents']")
        ABOUT = (By.XPATH, "//nav/ul/li[text()='About']")
        CONTACT = (By.XPATH, "//nav/ul/li[text()='Contact']")
        MY_ACCOUNT = (By.XPATH, "//nav/ul/li[text()='My Account']")
        LOGIN = (By.XPATH, "//nav/ul/li[text()='Login']")

    class HEADER(object):
        HEADER_LOGO=(By.TAG_NAME, "h1")

        SEARCH_DIV = (By.ID, "search-box")
        SEARCH_TEXT = (By.CSS_SELECTOR, "form#search-form >input#search")
        SEARCH_BUTTON = (By.CSS_SELECTOR, "form#search-form >button#search-submit")

    class PRODUCT(object):
        MAIN = (By.ID, "main")

        LEFT = (By.CLASS_NAME, "left")
        TITLE = (By.CSS_SELECTOR, "div#product-kit-description h3")
        DESCRIPTION = (By.CSS_SELECTOR, "div#product-kit-description p")
        SKU = (By.CSS_SELECTOR, "div#product-kit-description p span.sku")
        KIT_COMPONENTS = (By.ID, "kit-components")

        RIGHT = (By.CLASS_NAME, "right")
        ITEM_SUMMARY=(By.ID, "item-summary")
        AVAILABILITY=(By.CSS_SELECTOR, "div#product-availability div#availability")
        PRICE=(By.ID, "product-price")
        PRICE_LINE=(By.ID, "price-line")
        DISCOUNT_QTY=(By.CSS_SELECTOR, "div#product-discount div.qty-needed")
        DISCOUNT_AMT=(By.CSS_SELECTOR, "div#product-discount div.disc-amount span")

        OPTIONS_FORM=(By.CSS_SELECTOR, "div#item-summary div#product-availability div#product-options form#product-options-form")
        OPTION_DIV=(By.CLASS_NAME, "jqTransformSelectWrapper")

        QTY_DIV=(By.CSS_SELECTOR, "div#item-summary div#product-availability div#qty-in-cart div#qty-counter")
        QTY_BOX=(By.ID, "product-qty")
        QTY_ASC=(By.CSS_SELECTOR, "div#counter-module div#qty-controls a#increment")
        QTY_DESC=(By.CSS_SELECTOR, "div#counter-module div#qty-controls a#decrease")

        ADD_TO_CART=(By.ID, "add-to-cart")

    class CART(object):
        FORM = (By.ID, "cart-form")
        CART = (By.ID, "cart")

        CART_ITEM = (By.CSS_SELECTOR, "ul#cart >li")
        TOTAL_PRICE = (By.CSS_SELECTOR, "div.product-price >div")
        UNIT_PRICE = (By.CSS_SELECTOR, "div.product-unit-price >div.price")
        QTY_BOX = (By.CSS_SELECTOR, "div.product-qty >input")
        QTY_UP = (By.CSS_SELECTOR, "div.product-qty ul li:nth(0) >a")
        QTY_DOWN = (By.CSS_SELECTOR, "div.product-qty ul li:nth(1) >a")
        QTY_DELETE = (By.CSS_SELECTOR, "div.product-qty a.qty-delete")
        TITLE = (By.CSS_SELECTOR, "div.product-title a")
        SKU = (By.CSS_SELECTOR, "div.product-title span.product-sku")
        OPTIONS = (By.CSS_SELECTOR, "div.product-options")

        SUBTOTAL_VALUE=(By.ID, "subtotal-value")
        ORDER_TOTAL_VALUE = (By.ID, "order-total-value")
        CHECKOUT = (By.ID, "checkout-button")

    class CHECKOUT(object):
        ACCOUNT_INFO = (By.ID, "account-information")
        PLACE_ORDER = (By.ID, "place-order")

        SHIPPING_ADDRESS = (By.ID, "shipping-address")
        FIRST_NAME = (By.CSS_SELECTOR, "input[title='First Name']")
        LAST_NAME = (By.CSS_SELECTOR, "input[title='Last Name']")
        COMPANY = (By.CSS_SELECTOR, "input[title^='Company']")
        EMAIL = (By.CSS_SELECTOR, "input[title='Email']")
        PHONE = (By.CSS_SELECTOR, "input[title='Phone']")
        ADDRESS = (By.CSS_SELECTOR, "input[title='Address']")
        ADDRESS_2 = (By.CSS_SELECTOR, "input[title^='Address 2']")
        COUNTRY = (By.CSS_SELECTOR, "a.selectBox.country-field.pie.selectBox-dropdown")
        ZIP_CODE = (By.CSS_SELECTOR, "input[title='Zip Code']")
        CITY = (By.CSS_SELECTOR, "input[title='City']")
        STATE = (By.CSS_SELECTOR, "a.selectBox.state-field.pie.selectBox-dropdown")

        SHIPPING_OPTIONS = (By.ID, "shipping-options")
        SHIPPING_OPTION_LIST = (By.ID, "shipping-option-list")

        PAYMENT_DETAILS = (By.ID, "payment-details")
        CC_NUMBER = (By.ID, "creditCardNumber")
        SECURITY_CODE = (By.ID, "securityCode")
        EXP_MONTH=(By.CSS_SELECTOR, "a[class*='expirationMonth'")
        EXP_YEAR=(By.CSS_SELECTOR, "a[class*='expirationYear'")

        ORDER_NAV = (By.ID, "order-nav")
        SUBTOTAL_VALUE = (By.CSS_SELECTOR, "li div#subtotal-value")
        TAX_VALUE = (By.CSS_SELECTOR, "li div#tax-value")
        ORDER_TOTAL = (By.CSS_SELECTOR, "li#order-total div#order-total-value")
        SHIPPING_VALUE = (By.CSS_SELECTOR, "li div#shipping-value")

    class CHECKOUT_RECEIPT(object):
        ORDER_ID = (By.ID, "order-id")
        ORDER_DATE = (By.ID, "order-date")
        SHIPPING_TO = (By.ID, "shipping-to")
        BILLING_TO = (By.ID, "billing-to")
        PAYMENT_METHOD = (By.ID, "payment-method")
        PAYMENT_METHOD = (By.ID, "payment-method")

        ORDER_DETAILS = (By.ID, "order-details")
        ORDER_CART = (By.CSS_SELECTOR, "div#order-details ul#cart")

        ORDER_TOTALS = (By.ID, "micro-order-totals")
        SUB_TOTAL_VALUE = (By.CSS_SELECTOR, "ul#micro-order-totals li div#subtotal-value")
        SHIPPING_VALUE = (By.CSS_SELECTOR, "ul#micro-order-totals li div#shipping-value")
        TAX_VALUE = (By.CSS_SELECTOR, "ul#micro-order-totals li div#tax-value")
        TOTAL_VALUE = (By.CSS_SELECTOR, "ul#micro-order-totals li div#order-total-value")
