# coding = utf8

import pytest
from airtest.core.api import *
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
def before_case_execute():
    print("Before test")
    yield before_case_execute
    print("After test")




