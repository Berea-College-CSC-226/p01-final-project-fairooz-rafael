######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: Create the class that contains all the product objects of the store, also initializing the inventory with file from products.txt
#
######################################################################
# Acknowledgements:
#
# Revised with ChatGPT
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

from product import *


class Inventory:
    """manages a collection of products, stock updates, and earnings."""
    def __init__(self, products=None):
        self.products = products if products else read_products_file("products.txt")
        self.total_earnings = 0

    def get_all(self):
        """returns a shallow copy of all product objects."""
        return list(self.products)

    def sell_product(self, code, quantity=1):
        """sells an item by its barcode and updates earnings."""
        for p in self.products:
            if p.upc.code == code:  # matches product by barcode
                if p.update_stock(quantity):  # checks and subtracts stock
                    self.total_earnings += p.upc.selling_price * quantity
                    print(quantity, p.upc.product_name, "sold")
                    return True
                return False  #if stock not sufficient

        print("Product", code, "not found!")
        return False

    def show_inventory(self):
        """shows the inventory."""
        print("Current Inventory:")
        for p in self.products:
            print(p.display_info())

    def show_summary(self):
        """shows the summary of the inventory."""
        print("Sales Summary")
        print("Total Earnings:", self.total_earnings)
        print("Products Sold:")
        for p in self.products:
            sold = p.initial_stock - p.stock # calculates sold amount based on initial stock
            print(p.upc.product_name, ":", sold, "sold")

    def add_product(self, name, cost, price, manu, stock):
        """adds a new product after validating inputs."""
        # Validation for tests
        if not name or not manu:
            raise ValueError("Name and manufacturer cannot be empty.")

        if cost < 0 or price < 0:
            raise ValueError("Cost and price must be positive.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        new_p = Product(
            code=generate_random_upc(),  # auto-generate upc for new product
            name=name,
            cost=cost,
            price=price,
            manu=manu,
            stock=stock
        )

        self.products.append(new_p)
        return new_p
def main():
    """Simple tester for creating inventory and trying methods"""

    products = read_products_file("products.txt")  # loads initial list from file
    store = Inventory(products)

    store.show_inventory()

    code = input("Enter barcode to sell: ")
    quantity = int(input("Enter quantity to sell: "))

    store.sell_product(code, quantity)
    store.show_inventory()
    store.show_summary()


if __name__ == "__main__":
    main()
