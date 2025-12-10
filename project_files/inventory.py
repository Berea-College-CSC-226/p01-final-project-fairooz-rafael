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

from product import *


class Inventory:
    def __init__(self, products=None):
        self.products = products if products else read_products_file("products.txt")
        self.total_earnings = 0

    def get_all(self):
        return list(self.products)

    def sell_product(self, code, quantity=1):
        for p in self.products:
            if p.upc.code == code:
                if p.update_stock(quantity):
                    self.total_earnings += p.upc.selling_price * quantity
                    print(quantity, p.upc.product_name, "sold")
                    return True
                return False

        print("Product", code, "not found!")
        return False

    def show_inventory(self):
        print("Current Inventory:")
        for p in self.products:
            print(p.display_info())

    def show_summary(self):
        print("Sales Summary")
        print("Total Earnings:", self.total_earnings)
        print("Products Sold:")
        for p in self.products:
            sold = p.initial_stock - p.stock
            print(p.upc.product_name, ":", sold, "sold")

    # def add_product(self, name, cost, price, manu, stock):
    #     # Auto-generate UPC (your preference from UPC class)
    #     new_p = Product(
    #         code=None,     # UPC class will auto-generate inside
    #         name=name,
    #         cost=cost,
    #         price=price,
    #         manu=manu,
    #         stock=stock
    #     )
    #     self.products.append(new_p)
    #     return new_p

    def add_product(self, name, cost, price, manu, stock):
        # Validation for tests
        if not name or not manu:
            raise ValueError("Name and manufacturer cannot be empty.")

        if cost < 0 or price < 0:
            raise ValueError("Cost and price must be positive.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        new_p = Product(
            code=None,
            name=name,
            cost=cost,
            price=price,
            manu=manu,
            stock=stock
        )

        self.products.append(new_p)
        return new_p
def main():
    products = read_products_file("products.txt")
    store = Inventory(products)

    store.show_inventory()

    code = input("Enter barcode to sell: ")
    quantity = int(input("Enter quantity to sell: "))

    store.sell_product(code, quantity)
    store.show_inventory()
    store.show_summary()


if __name__ == "__main__":
    main()
