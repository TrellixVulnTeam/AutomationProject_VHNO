# coding = utf8
import os
from time import sleep

from page.system.system import System, logger

os.path.abspath(".")


"""
    @File:contacts_page.py
    @Author:Bruce
    @Date:2021/1/13
"""


class Contacts_Page(System):

    # Ui element
    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.save = self.poco("com.google.android.contacts:id/save_button")

    def start_contacts(self):
        self.device.start_app("com.google.android.contacts")
        sleep(1)

    def stop_contacts(self):
        sleep(1)
        self.device.stop_app("com.google.android.contacts")

    def create_contact(self, contact_name="Test", phone_number="18512026630"):
        self.device.shell("am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/"
                          "contact -e name %s -e phone %s" % (contact_name, phone_number))
        return contact_name, phone_number
