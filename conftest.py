# coding = utf8
import os

import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException
from time import sleep
os.path.abspath(".")

"""
    @File:conftest.py
    @Author:Bruce
    @Date:2020/12/15
"""

"""
    a py file which saved pytest's fixture for use
"""


@pytest.fixture(scope = "function")
def Device():
    print("Before test")
    yield Device
    print("After test")




