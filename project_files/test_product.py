######################################################################
# Author:  FairoozRafael,
# Username: hermozafreitasr, tasniaf
#
# Purpose: Create a product class to have it in an inventory store and inherit the UPC class which holds the unique barcode and details of the product
#
######################################################################
# Acknowledgements:
#
# None: Original work

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import os

from product import *
from upc import *


products = read_products_file("products.txt")
assert len(products) == 3

p1, p2, p3 = products


assert p1.product_name == "SamSi TV"
assert p1.product_cost == 300
assert p1.selling_price == 500
assert p1.manufacturer == "SamSi"
assert p1.stock == 15


assert p2.product_name == "iPhone xoxo"
assert p2.selling_price == 999
assert p2.stock == 25


assert p3.product_name == "PlayStation flip"
assert p3.product_cost == 400
assert p3.stock == 10

print("read_products_file() tests passed")



p_test = Product(code=generate_random_upc(), name="Test", cost=10, price=20, manu="Demo", stock=5)

for i in range(3):
    last_stock = p_test.stock
    ok = p_test.update_stock(1)
    assert ok is True
    assert p_test.stock == last_stock - 1
    print("Stock updated successfully:", last_stock, "to", p_test.stock)


last_stock = p_test.stock
ok = p_test.update_stock(10)
assert ok is False
assert p_test.stock == last_stock
print("Failed stock update test passed")


code = generate_random_upc()
assert len(code) == 12
assert code.isdigit()
print("UPC generation test passed")