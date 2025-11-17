from hw09_upc_start import *

from inspect import getframeinfo, stack

def unittest(did_pass):
    """
    Print the result of a unit test.

    :param did_pass: a boolean representing the test
    :return: None
    """

    caller = getframeinfo(stack()[1][0])
    linenum = caller.lineno
    if did_pass:
        msg = "Test at line {0} ok.".format(linenum)
    else:
        msg = ("Test at line {0} FAILED.".format(linenum))
    print(msg)


def a09_test_suite():
    # We have began your test suite here. You should add more as you develop fruitful functions!
    unittest(is_valid_input("036000291452") == True)
    unittest(is_valid_input("1") == False)
    unittest(is_valid_input("036001456789") == True)
    unittest(is_valid_modulo("036000291452") == True)
    unittest(is_valid_modulo("036001456789") == True)
    unittest(translate("3", 3) == "0111101")
    unittest(translate("3", 7) == "1000010")


if __name__ == "__main__":
    a09_test_suite()
