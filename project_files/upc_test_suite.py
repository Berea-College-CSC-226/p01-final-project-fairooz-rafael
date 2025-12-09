######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: Create a barcode class to have it associated with a unique product in an inventory store
#
######################################################################
# Acknowledgements:
#
# None: Original work

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################
from upc import *
import sys
from inspect import getframeinfo, stack


def unittest(did_pass):
    """
    Print the result of a unit test.
    """
    caller = getframeinfo(stack()[1][0])
    linenum = caller.lineno
    if did_pass:
        msg = f"Test at line {linenum} ok."
    else:
        msg = f"Test at line {linenum} FAILED."
    print(msg)


def a09_test_suite():
    print("Running UPC Test Suite...\n")

    # -------------------------------
    # TEST: is_valid_input()
    # -------------------------------
    u1 = UPC("036000291452")
    unittest(u1.is_valid_input() == True)

    u2 = UPC("1")
    unittest(u2.is_valid_input() == False)

    u3 = UPC("ABCDEFGHIJKL")
    unittest(u3.is_valid_input() == False)

    u4 = UPC("123456789012")
    unittest(u4.is_valid_input() == True)

    # -------------------------------
    # TEST: is_valid_modulo()
    # Using real correct UPC: 036000291452 (valid)
    # -------------------------------
    u5 = UPC("036000291452")
    unittest(u5.is_valid_modulo() == True)

    # Invalid last digit
    u6 = UPC("036000291453")
    unittest(u6.is_valid_modulo() == False)

    # -------------------------------
    # TEST: translate()
    # -------------------------------
    temp = UPC("123456789012")

    # left side (pos 1–6)
    unittest(temp.translate("0", 1) == "0001101")
    unittest(temp.translate("9", 6) == "0001011")

    # right side (pos 7–12)
    unittest(temp.translate("0", 7) == "1110010")
    unittest(temp.translate("9", 12) == "1110100")

    # -------------------------------
    # TEST: generate_random_upc()
    # -------------------------------
    for _ in range(5):
        code = generate_random_upc()
        u = UPC(code)

        # Should be 12 digits
        unittest(len(code) == 12)
        unittest(code.isdigit() == True)

        # Must pass modulo validation
        unittest(u.is_valid_modulo() == True)

    # -------------------------------
    # TEST: automatic generation inside UPC()
    # -------------------------------
    auto = UPC()
    unittest(len(auto.code) == 12)
    unittest(auto.code.isdigit() == True)
    unittest(auto.is_valid_modulo() == True)

    print("\nTest Suite Complete.")


if __name__ == "__main__":
    a09_test_suite()
