# coding = utf8
import os

os.path.abspath(".")
"""
    @Project:AutomationProject
    @File:save2txt.py
    @Author:十二点前要睡觉
    @Date:2022/2/18 17:42
"""


def toTxt(result):
    print(type(result))
    if type(result) == list:
        for i in result:
            with open("./Result.txt", "a+") as f:
                f.write(str(i) + "\n")
    else:
        with open("./Result.txt", "a+") as f:
            f.write(str(result) + "\n")
