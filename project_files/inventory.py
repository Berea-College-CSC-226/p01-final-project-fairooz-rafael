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
        if products is None:
            self.products = read_products_file("products.txt")  #initial changes of generating the list of objects from here
        else:
            self.products = products
        self.total_earnings = 0

    # def get_all(self):
    #     return list(self.products)
    def sell_product(self, code, quantity=1):
        for product in self.products:
            if product.code == code:
                if product.update_stock(quantity):
                    self.total_earnings += product.selling_price * quantity
                    print(quantity, product.product_name, "sold")
                    return True
                else:
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
            sold_quantity = p.initial_stock - p.stock
            print(p.product_name, ":", sold_quantity, "sold")

def main():
    filename = input("Enter product file: ").strip()
    if not os.path.isfile(filename):
        print(filename, "not found! Using default 'products.txt'")
        filename = "products.txt"

    #products = read_products_file(filename)

    store = Inventory()


    store.show_inventory()

    code = input("Enter barcode to sell: ")
    quantity = int(input("Enter quantity to sell: "))
    store.sell_product(code, quantity)

    store.show_inventory()
    store.show_summary()


if __name__ == "__main__":
    main()