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

from inventory import *

class CompanyExpenses(Inventory):
    def __init__(self, rent=500, salaries=900, other=150):
        super().__init__()
        self.fixed_expenses = {
            "Rent": rent,
            "Salaries": salaries,
            "Other": other
        }

    def get_expenses_dict(self):
        original_cost = sum(
            (p.initial_stock - p.stock) * p.product_cost
            for p in self.products  #what's going on here?
        )

        expenses = {
            "Revenue": self.total_earnings,
            "Original Cost": original_cost
        }

        expenses.update(self.fixed_expenses)
        return expenses

    def percentages(self):
        expenses = self.get_expenses_dict()
        total = sum(expenses.values())
        result = {}
        for k, v in expenses.items():
            if total > 0:
                result[k] = v / total * 100
            else:
                result[k] = 0
        return result

    def show_summary(self):
        expenses = self.get_expenses_dict()
        print("Company Expenses Summary")
        for k, v in expenses.items():
            print(k, v)
        print("Total", sum(expenses.values()))
        print("Percentages:")
        for k, v in self.percentages().items():
            print(k, v)

def main():
    company = CompanyExpenses(rent=800, salaries=1200)

    company.show_inventory()

    code = input("Enter barcode to sell: ")
    quantity = int(input("Enter quantity to sell: "))
    company.sell_product(code, quantity)

    company.show_inventory()
    company.show_summary()

if __name__ == "__main__":
    main()