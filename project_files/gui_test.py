######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: Create the graphic interface that contains all the functions for our program
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

from product import Product, read_products_file
from inventory import Inventory


# -----------------------------
# Main GUI Application
# -----------------------------
class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping System Prototype")

        self.inventory = Inventory()   # uses your file-based loading
        self.cart = []

        self.build_user_select()

    # -----------------------------
    # Page 1 — User Type Selection
    # -----------------------------
    def build_user_select(self):
        self.clear() #whipes all the elements we had before to write something like a new screen

        tk.Label(self.root, text="Select User Type", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Customer", width=20, height=2,
                  command=self.build_customer_main).pack(pady=10)

        #implement the company user here
            #also create the method for login in before seeing a company's interface

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

        self.product_list = tk.Listbox(frame, width=60, height=10)
        self.product_list.grid(row=1, column=0)

        # Load product info into list
        for p in self.inventory.products:
            line = (
                f"{p.code} | {p.product_name} - ${p.selling_price:.2f} "
                f"| Stock: {p.stock}"
            )
            self.product_list.insert(tk.END, line)

        tk.Button(frame, text="Add to Cart", command=self.add_to_cart).grid(row=2, column=0, pady=10)

        tk.Button(self.root, text="View Cart / Checkout", width=20,
                  command=self.build_cart_page).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.build_user_select).pack(pady=5)

    # -----------------------------
    # Add Selected Product to Cart
    # -----------------------------
    def add_to_cart(self):
        selection = self.product_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a product.")
            return

        index = selection[0]
        product = self.inventory.products[index]

        # Check stock
        if product.stock <= 0:
            messagebox.showerror("Out of Stock", f"{product.product_name} is unavailable.")
            return

        # Reduce stock in inventory
        product.update_stock(1)
        #global have_cart = True
        #send a signal that tells us whether or not there's something in the cart, so that the stock update avoid fake purchases
        self.cart.append(product)

        messagebox.showinfo("Added", f"{product.product_name} added to cart!")

        # Refresh product list
        self.build_customer_main()

    # -----------------------------
    # Page 3 — Cart and Checkout
    # -----------------------------
    def build_cart_page(self):
        self.clear()

        tk.Label(self.root, text="Your Cart", font=("Arial", 16)).pack(pady=10)

        cart_box = tk.Listbox(self.root, width=50, height=8)
        cart_box.pack()

        total_price = 0

        for p in self.cart:
            cart_box.insert(tk.END, f"{p.product_name} - ${p.selling_price:.2f}")
            total_price += p.selling_price

        tk.Label(self.root, text=f"Total: ${total_price:.2f}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Confirm Purchase",
                  command=lambda: self.checkout(total_price)).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.build_customer_main).pack(pady=5)
        ##here check if there's something in the cart and hasn't been paid, wipe that off

    # -----------------------------
    # Final Checkout
    # -----------------------------
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
    root.geometry("450x550")
    app = ShoppingApp(root)
    root.mainloop()


