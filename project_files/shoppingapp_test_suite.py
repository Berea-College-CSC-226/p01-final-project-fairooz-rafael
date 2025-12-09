# --------------------------------------------------
# TEST SUITE FOR SHOPPINGAPP
# --------------------------------------------------

import types

# -----------------------------
# MOCK TKINTER + MESSAGEBOX
# -----------------------------
class MockWidget:
    def destroy(self): pass

class MockListbox(MockWidget):
    def __init__(self):
        self.items = []
        self.selection = []

    def insert(self, index, value):
        self.items.append(value)

    def curselection(self):
        return self.selection

    def set_selection(self, index):
        self.selection = [index]


class MockTk:
    def __init__(self):
        self._children = []

    def winfo_children(self):
        return self._children

    def title(self, x): pass


class MockMessageBox:
    last = None
    def showinfo(title, msg):
        MockMessageBox.last = ("info", title, msg)
    def showwarning(title, msg):
        MockMessageBox.last = ("warning", title, msg)
    def showerror(title, msg):
        MockMessageBox.last = ("error", title, msg)


# -----------------------------
#   MOCK INVENTORY & PRODUCTS
# -----------------------------
class MockProduct:
    def __init__(self, code, name, price, stock):
        self.code = code
        self.product_name = name
        self.selling_price = price
        self.stock = stock

    def update_stock(self, q):
        self.stock -= q


class MockInventory:
    def __init__(self):
        self.products = [
            MockProduct("111111111111", "Apple", 1.25, 10),
            MockProduct("222222222222", "Water", 0.99, 5)
        ]
        self.total_earnings = 0


# -----------------------------
# IMPORT THE SHOPPINGAPP FILE
# -----------------------------
from gui_test import *  # <–– rename if your file name is different

# Patch tkinter and messagebox inside shoppingapp
shoppingapp.tk = types.SimpleNamespace()
shoppingapp.tk.Tk = MockTk
shoppingapp.tk.Frame = MockWidget
shoppingapp.tk.Label = lambda *a, **k: MockWidget()
shoppingapp.tk.Button = lambda *a, **k: MockWidget()
shoppingapp.tk.Listbox = lambda *a, **k: MockListbox()
shoppingapp.tk.Entry = lambda *a, **k: types.SimpleNamespace(get=lambda: "")

shoppingapp.messagebox = MockMessageBox
shoppingapp.Inventory = MockInventory


# -----------------------------
# SIMPLE TEST HELPER
# -----------------------------
def unittest(condition):
    import inspect
    line = inspect.currentframe().f_back.f_lineno
    if condition:
        print(f"> OK  (line {line})")
    else:
        print(f"> FAIL (line {line})")


# --------------------------------------------------
# START TESTS
# --------------------------------------------------
def run_tests():

    print("\n===== RUNNING SHOPPINGAPP TEST SUITE =====\n")

    # -----------------------------------------
    # Create app with mocks
    # -----------------------------------------
    root = MockTk()
    app = shoppingapp.ShoppingApp(root)

    # -----------------------------------------
    # 1. Initial app state
    # -----------------------------------------
    unittest(len(app.cart) == 0)
    unittest(len(app.inventory.products) == 2)

    # -----------------------------------------
    # 2. Simulate product list + selection
    # -----------------------------------------
    first_product = app.inventory.products[0]
    old_stock = first_product.stock

    mock_list = MockListbox()
    mock_list.items = ["dummy"]
    mock_list.set_selection(0)

    app.product_list = mock_list
    app.add_to_cart()

    unittest(len(app.cart) == 1)
    unittest(first_product.stock == old_stock - 1)
    unittest(MockMessageBox.last[0] == "info")

    # -----------------------------------------
    # 3. Navigating back should NOT change stock
    # -----------------------------------------
    s_before = first_product.stock
    app.build_customer_main()
    unittest(first_product.stock == s_before)

    # -----------------------------------------
    # 4. Checkout clears cart + adds earnings
    # -----------------------------------------
    total = sum(p.selling_price for p in app.cart)
    app.checkout(total)

    unittest(len(app.cart) == 0)
    unittest(app.inventory.total_earnings == total)

    # -----------------------------------------
    # 5. Test LOGIN FUNCTION
    # -----------------------------------------
    app.build_company_login()

    # Extract attempt_login closure
    # located inside build_company_login
    for v in app.__dict__.values():
        if callable(v) and hasattr(v, "__name__") and v.__name__ == "attempt_login":
            attempt_login = v
            break

    # Test correct credentials
    MockMessageBox.last = None
    attempt_login("admin", "1234")
    unittest(MockMessageBox.last[0] == "info")

    # Test incorrect credentials
    MockMessageBox.last = None
    attempt_login("wrong", "00")
    unittest(MockMessageBox.last[0] == "error")

    print("\n===== TESTS COMPLETE =====\n")


if __name__ == "__main__":
    run_tests()
