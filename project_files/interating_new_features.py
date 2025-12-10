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

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from product import Product, read_products_file
from inventory import Inventory
from graphics_interface_for_company import *   # <-- ADD THIS


# -----------------------------
# Main GUI Application
# -----------------------------
class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping System Prototype")

        self.inventory = Inventory()
        self.company = CompanyExpenses()   # <-- Uses same file-based product loading

        # Sync inventory into company tracker:
        self.company.products = self.inventory.products

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

        tk.Button(self.root, text="Company", width=20, height=2,
                  command=self.build_company_login).pack(pady=10)


    # -----------------------------
    # Company Login
    # -----------------------------
    def build_company_login(self):
        self.clear()

        tk.Label(self.root, text="Company Login", font=("Arial", 18)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username == "admin" and password == "1234":
                messagebox.showinfo("Welcome", "Login successful.")
                self.build_company_main()
            else:
                messagebox.showerror("Access Denied", "Incorrect credentials.")

        tk.Button(self.root, text="Login", width=15,
                  command=attempt_login).pack(pady=10)

        tk.Button(self.root, text="Back",
                  command=self.build_user_select).pack(pady=5)


    # -----------------------------
    # Company Dashboard
    # -----------------------------
    def build_company_main(self):
        self.clear()

        tk.Label(self.root, text="Company Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="View Inventory", width=20, height=2,
                  command=self.build_company_inventory).pack(pady=10)

        tk.Button(self.root, text="View Sales Summary", width=20, height=2,
                  command=self.build_sales_summary).pack(pady=10)

        tk.Button(self.root, text="View Expense Pie Chart", width=20, height=2,
                  command=self.build_company_expenses_chart).pack(pady=10)

        tk.Button(self.root, text="Back", width=20,
                  command=self.build_user_select).pack(pady=20)


    # -----------------------------
    # Inventory view
    # -----------------------------
    def build_company_inventory(self):
        self.clear()
        tk.Label(self.root, text="Inventory Overview", font=("Arial", 18)).pack(pady=10)

        box = tk.Listbox(self.root, width=60, height=12)
        box.pack(pady=5)

        for p in self.inventory.products:
            line = f"{p.product_name} | ${p.selling_price:.2f} | Stock: {p.stock}"
            box.insert(tk.END, line)

        tk.Button(self.root, text="Back", command=self.build_company_main).pack(pady=10)


    # -----------------------------
    # Sales Summary
    # -----------------------------
    def build_sales_summary(self):
        self.clear()
        tk.Label(self.root, text="Sales Summary", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text=f"Total Earnings: ${self.inventory.total_earnings:.2f}",
                 font=("Arial", 14)).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.build_company_main).pack(pady=20)


    # -----------------------------
    # NEW: Expense Pie Chart
    # -----------------------------
    def build_company_expenses_chart(self):
        self.clear()

        tk.Label(self.root, text="Expense Distribution", font=("Arial", 18)).pack(pady=10)

        # Sync inventory values again
        self.company.products = self.inventory.products
        self.company.total_earnings = self.inventory.total_earnings

        percentages = self.company.percentages()
        labels = list(percentages.keys())
        values = list(percentages.values())

        # Draw chart
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("Company Expense Breakdown")

        # Tkinter embedding
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        plt.close(fig)

        tk.Button(self.root, text="Back",
                  command=self.build_company_main).pack(pady=10)


    # -----------------------------
    # Customer Shopping
    # -----------------------------
    def build_customer_main(self):
        self.clear()

        tk.Label(self.root, text="Welcome, Customer!", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Available Products:").grid(row=0, column=0)

        self.product_list = tk.Listbox(frame, width=60, height=10)
        self.product_list.grid(row=1, column=0)

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
    # Add to Cart
    # -----------------------------
    def add_to_cart(self):
        selection = self.product_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a product.")
            return

        index = selection[0]
        product = self.inventory.products[index]

        if product.stock <= 0:
            messagebox.showerror("Out of Stock", f"{product.product_name} is unavailable.")
            return

        product.update_stock(1)
        self.cart.append(product)

        messagebox.showinfo("Added", f"{product.product_name} added to cart!")

        self.build_customer_main()


    # -----------------------------
    # Cart Page
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


    # -----------------------------
    # Checkout
    # -----------------------------
    def checkout(self, total):
        messagebox.showinfo("Thank you!", f"Purchase complete!\nTotal: ${total:.2f}")

        # Register earnings
        self.inventory.total_earnings += total

        self.cart = []
        self.build_customer_main()


    # -----------------------------
    # Utility — clear window
    # -----------------------------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x650")
    app = ShoppingApp(root)
    root.mainloop()
