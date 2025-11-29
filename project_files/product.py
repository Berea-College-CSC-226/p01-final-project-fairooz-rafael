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
from upc import UPC


class Product(UPC):
    def __init__(self, code=None, name=None, cost=None, price=None, manu=None, stock=0):
        super().__init__(code, name, cost, price, manu)  # inherit UPC attributes
        self.stock = stock
        self.initial_stock = stock

    def update_stock(self, quantity):

        if quantity <= self.stock:
            self.stock -= quantity
            return True
        else:
            print("Not available")
            return False

    def display_info(self):

        return ("Name:", self.product_name,
                "Price:", self.selling_price,
                "Barcode:", self.code,
                "Stock:", self.stock)

def read_products_file(filename):
        if not os.path.isfile(filename):
            print(filename, "not found!")
            return []

        products = []
        with open(filename, 'r') as file_content:
            num_products = int(file_content.readline().strip())

            for _ in range(num_products):
                product_data = []

                for i in range(6):
                    content = file_content.readline().strip("\n")
                    key, value = content.split(":", 1)

                    if key in ["Cost", "Price"]:
                        value = float(value)
                    elif key == "Stock":
                        value = int(value)

                    product_data.append(value)

                p = Product(code=product_data[5], name=product_data[0], cost=product_data[1],
                            price=product_data[2], manu=product_data[3], stock=product_data[4])  #the object is being created with the file values
                products.append(p)

        return products

def main():
        filename = input("Enter product file: ").strip()
        if not os.path.isfile(filename):
            print(filename, "not found! Using default 'products.txt'")
            filename = "products.txt"

        products = read_products_file(filename)   #right here we need to do the cnnection with the inventory class

        print("Products available:")
        for p in products:
            print(p.display_info())

if __name__ == "__main__":
    main()