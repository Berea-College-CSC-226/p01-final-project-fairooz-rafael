from inventory import Inventory
from gui import ShoppingApp

def main():
    store = Inventory("products.txt")
    ShoppingApp(store).run()

if __name__ == "__main__":
    main()
