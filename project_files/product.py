######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: Create the class skeleton for a product in the store
#
######################################################################
# Acknowledgements:
# upc class homework

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import os

from project_files.upc import generate_random_upc
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
    with open(filename, 'r', encoding='utf-8') as file_content:
        # read first non-empty line and parse number of products
        first = ""
        while first.strip() == "":
            first = file_content.readline()
            if first == "":
                # empty file
                return []
        num_products = int(first.strip())

        for _ in range(num_products):
            product_data = []

            # read exactly 5 non-empty lines for each product
            lines_read = 0
            while lines_read < 5:
                content = file_content.readline()
                if not content:
                    break
                content = content.strip("\n").strip()
                if content == "":
                    continue
                # split into key/value with maxsplit=1
                if ":" in content:
                    key, value = content.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                else:
                    # fallback: treat whole line as value
                    key, value = None, content.strip()

                if key in ["Cost", "Price"]:
                    try:
                        value = float(value)
                    except Exception:
                        value = 0.0
                elif key == "Stock":
                    try:
                        value = int(value)
                    except Exception:
                        value = 0
                # keep the raw value otherwise (Name, Manufacturer)
                product_data.append(value)
                lines_read += 1

            # product_data should now contain [Name, Cost, Price, Manufacturer, Stock]
            if len(product_data) == 5:
                p = Product(code=generate_random_upc(),
                            name=product_data[0],
                            cost=product_data[1],
                            price=product_data[2],
                            manu=product_data[3],
                            stock=product_data[4])
                products.append(p)
            else:
                # malformed product entry; skip
                print("[WARN] malformed product entry, skipping:", product_data)

    return products


def main():
    filename = input("Enter product file: ").strip()
    if not os.path.isfile(filename):
        print(filename, "not found! Using default 'products.txt'")
        filename = "products.txt"

    products = read_products_file(filename)

    print("Products available:")
    for p in products:
        print(p.display_info())


if __name__ == "__main__":
    main()
