__author__ = 'EpiCenter'

from selenium.common.exceptions import TimeoutException

class TimeoutException(TimeoutException):
    def __init__(self, element):
        """ Initialize the object"""
        self.element = element
        self.message = "Unable to find element '%s'" % self.element

    def __str__(self):
        return repr(self.message)
