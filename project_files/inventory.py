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

#inventory needs a method that count how many repeated objects exists, but let's assume we have 15 tvs, we need 15 different objects
#we count the stock based on the name, because they can have indeed the same name

# def update_stock(self, quantity):
#     if quantity <= self.stock:
#         self.stock -= quantity
#         return True
#     else:
#         print("Not available")
#         return False

#the way to do this is going through the list of all products and using acumulators
#its going to be either a dictionary or a list but i like dictionary more
#plus the good thing about a dictionary is that i already have the key which is the name of the product
#stock = {"obj1": result_of_counting}

class Inventory:
    def __init__(self, products=None):
        if products is None:
            self.products = read_products_file("products.txt")  #filling using the method that returns a list of all objects
        else:
            self.products = products
        self.total_earnings = 0
        self.accumulator = {} #this works as stock for now

    def check_inventory(self):
        for product in self.products: #product is a Product object
            if product.product_name in self.accumulator:
                self.accumulator[product.product_name] += 1
            else:
                self.accumulator[product.product_name] = 1

            #in order to make stock a value that can be modified it needs to be part of the class


    def sell_product(self, code, quantity=1):
        for product in self.products: #self.products = list of all products
            if product.code == code: #this is the part where scanning the UPC barcode would happen because otherwise it's pointless to use the code
                #since the product is inside a list we can easily drop the product from this list, now what about the text file?
                # this part must read through the text file again?
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

    def show_summary(self): #this may probably be renamed
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
    store.check_inventory()
    print(store.accumulator) #reading inventory working properly


    code = input("Enter barcode to sell: ")
    quantity = int(input("Enter quantity to sell: "))
    store.sell_product(code, quantity)

    store.show_inventory()


    store.show_summary()


if __name__ == "__main__":
    main()