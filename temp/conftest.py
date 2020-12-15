# coding = utf8
import os

os.path.abspath(".")
"""
    @File:conftest.py
    @Author:Bruce
    @Date:2020/12/15
"""

from time import sleep
import pytest

"""
    a py file which saved pytest's fixture for use
"""


@pytest.fixture(scope="function")
def before_case_execute():
    sleep(2)
    yield before_case_execute
    sleep(2)
