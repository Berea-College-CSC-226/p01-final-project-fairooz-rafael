from product import *
from inventory import *


products = read_products_file("products.txt")
store = Inventory(products)


all_products = store.get_all()
assert len(all_products) == 3
assert all_products[0].product_name == "SamSi TV"
assert all_products[1].product_name == "iPhone xoxo"
assert all_products[2].product_name == "PlayStation flip"
print("get_all() test passed")

p1_code = products[0].code
initial_stock = products[0].stock
initial_earnings = store.total_earnings

ok = store.sell_product(p1_code, 2)
assert ok is True
assert products[0].stock == initial_stock - 2
assert store.total_earnings == initial_earnings + products[0].selling_price * 2
print("sell_product() success test passed")


ok = store.sell_product(p1_code, 1000)
assert ok is False
assert products[0].stock == initial_stock - 2
print("sell_product() failure test passed")


ok = store.sell_product("000000000000", 1)
assert ok is False
print("sell_product() invalid code test passed")


sold_quantity = products[0].initial_stock - products[0].stock
assert sold_quantity == 2
assert store.total_earnings == products[0].selling_price * 2
print("Summary calculation test passed")