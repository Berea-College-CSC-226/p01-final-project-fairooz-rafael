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
import random

class UPC:
    """Simple container class for UPC attributes."""
    def __init__(self, code, name, cost, price, manufacturer):
        self.code = code
        self.product_name = name
        self.product_cost = cost
        self.selling_price = price
        self.manufacturer = manufacturer


def generate_random_upc():
    """Generates a valid random UPC-A code (12 digits with valid checksum)."""
    digits = [random.randint(0, 9) for _ in range(11)]

    odd_sum = sum(digits[0:11:2])
    even_sum = sum(digits[1:11:2])

    check = (10 - ((odd_sum * 3 + even_sum) % 10)) % 10
    digits.append(check)

    return ''.join(str(d) for d in digits)
