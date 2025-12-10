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
import tkinter as tk
from tkinter import ttk, messagebox


# -----------------------------
# Product Class (simplified UPC class)
# -----------------------------
class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.name} (${self.price})"


# -----------------------------
# Inventory Class
# -----------------------------
class Inventory:
    def __init__(self):
        # Preloaded items
        self.products = {
            "123456789012": Product("123456789012", "Milk", 3.99),
            "987654321098": Product("987654321098", "Bread", 2.49),
            "111222333444": Product("111222333444", "Eggs", 4.50),
            "555666777888": Product("555666777888", "Cheese", 5.25),
        }

    def get_all(self):
        return list(self.products.values())


# -----------------------------
# Main GUI Application
# -----------------------------
class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping System Prototype")

        self.inventory = Inventory()
        self.cart = []

        self.build_user_select()

    # -----------------------------
    # Page 1 — User Type Selection
    # -----------------------------
    def build_user_select(self):
        self.clear()

        tk.Label(self.root, text="Select User Type", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Customer", width=20, height=2,
                  command=self.build_customer_main).pack(pady=10)

        tk.Button(self.root, text="Company (disabled)", width=20, height=2, state="disabled").pack(pady=10)

    # -----------------------------
    # Page 2 — Customer Shopping Page
    # -----------------------------
    def build_customer_main(self):
        self.clear()

        tk.Label(self.root, text="Welcome, Customer!", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Products List
        tk.Label(frame, text="Available Products:").grid(row=0, column=0)

        self.product_list = tk.Listbox(frame, width=40, height=8)
        self.product_list.grid(row=1, column=0)

        for p in self.inventory.get_all():
            self.product_list.insert(tk.END, f"{p.code} | {p.name} - ${p.price}")

        tk.Button(frame, text="Add to Cart", command=self.add_to_cart).grid(row=2, column=0, pady=10)

        # View Cart
        tk.Button(self.root, text="View Cart / Checkout", width=20,
                  command=self.build_cart_page).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.build_user_select).pack(pady=5)

    def add_to_cart(self):
        selection = self.product_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a product.")
            return

        index = selection[0]
        product = self.inventory.get_all()[index]
        self.cart.append(product)

        messagebox.showinfo("Added", f"{product.name} added to cart!")

    # -----------------------------
    # Page 3 — Cart and Checkout
    # -----------------------------
    def build_cart_page(self):
        self.clear()

        tk.Label(self.root, text="Your Cart", font=("Arial", 16)).pack(pady=10)

        cart_box = tk.Listbox(self.root, width=40, height=8)
        cart_box.pack()

        total_price = 0

        for p in self.cart:
            cart_box.insert(tk.END, f"{p.name} - ${p.price}")
            total_price += p.price

        tk.Label(self.root, text=f"Total: ${total_price:.2f}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Confirm Purchase",
                  command=lambda: self.checkout(total_price)).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.build_customer_main).pack(pady=5)

    def checkout(self, total):
        messagebox.showinfo("Thank you!", f"Purchase complete!\nTotal: ${total:.2f}")
        self.cart = []
        self.build_customer_main()

    # -----------------------------
    # Utility: Clear Screen
    # -----------------------------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    app = ShoppingApp(root)
    root.mainloop()
