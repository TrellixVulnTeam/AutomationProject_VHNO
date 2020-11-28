import os
os.path.abspath(".")
import pytest

# 装饰器从session -> module -> class -> function
def add(x):
    return x + 1

# def test_add(before_each_case):
def test_add(before_case_execute):
    assert add(3) == 4

if __name__ == "__main__":
    pytest.main()

