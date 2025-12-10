######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: Run the official software that displays our graphic interface for a shopping application
#
######################################################################
# Acknowledgements:
# Tkinter library
# Listbox, and Scrollbar documentation
# google
# ChatGPT
#

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from inventory import Inventory
from product import Product, read_products_file
from graphics_interface_for_company import CompanyExpenses



# Main Shopping GUI Application

class ShoppingApp:
    """
    ShoppingApp is the main GUI controller for our prototype.

    Handles both customer and company interfaces:
    - Customer: browse products, add to cart, checkout.
    - Company: login, view inventory, add products, view sales and expenses.

    Attributes:
        root (tk.Tk): The root Tkinter window.
        inventory (Inventory): Tracks products and earnings.
        company (CompanyExpenses): Tracks company-related expenses.
        cart (list): Temporary storage for products added by customers.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Shopping System Prototype")
        self.root.configure(bg="#1c1c1c")
        self.root.resizable(True, True)

        self.inventory = Inventory()
        self.company = CompanyExpenses()

        # sync company tracker with inventory
        self.company.products = self.inventory.products
        self.company.total_earnings = self.inventory.total_earnings

        self.cart = []  # stores items in format {"product": Product, "quantity": int}

        # start app at user selection page
        self.build_user_select()

    # Helper: styled button

    def app_button(self, master, text, command):
        """
        Returns a consistently styled Tkinter Button.
        We're using this instead of repeating style code everywhere.
        Could switch to ttk.Button for theme support.
        """
        return tk.Button(
            master,
            text=text,
            width=25,
            height=2,
            bg="#8B0000",
            fg="white",
            font=("Helvetica", 12, "bold"),
            activebackground="#A52A2A",
            activeforeground="white",
            command=command
        )

    # User selection page

    def build_user_select(self):
        """
        First page of the app. Choose between Customer and Company.
        """
        self.clear()
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, padx=20, pady=50)
        tk.Label(frame, text="Welcome to Amigazon Shopping", font=("Helvetica", 30, "bold"),
                 bg="#2c2c2c", fg="white").pack(pady=30)
        tk.Label(frame, text="Select User Type", font=("Helvetica", 24, "bold"),
                 bg="#2c2c2c", fg="white").pack(pady=30)

        self.app_button(frame, "Customer", self.build_customer_main).pack(pady=15)
        self.app_button(frame, "Company", self.build_company_login).pack(pady=15)


    # Company login

    def build_company_login(self):
        """
        Company login page with username/password.
        Right now credentials are hardcoded, could move to file/db later.
        """
        self.clear()
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, padx=20, pady=50)

        tk.Label(frame, text="Company Login", font=("Helvetica", 20, "bold"),
                 bg="#2c2c2c", fg="white").pack(pady=20)

        input_frame = tk.Frame(frame, bg="#2c2c2c")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Username:", bg="#2c2c2c", fg="white").grid(row=0, column=0, sticky="e", padx=5,
                                                                               pady=5)
        username_entry = tk.Entry(input_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Password:", bg="#2c2c2c", fg="white").grid(row=1, column=0, sticky="e", padx=5,
                                                                               pady=5)
        password_entry = tk.Entry(input_frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        def attempt_login():
            """
            Check credentials and move to company dashboard.
            Simple logic for now; could integrate hashed passwords or database.
            """
            username = username_entry.get()
            password = password_entry.get()
            if username == "admin" and password == "1234":
                messagebox.showinfo("Welcome", "Login successful.")
                self.build_company_main()
            else:
                messagebox.showerror("Access Denied", "Incorrect credentials.")

        self.app_button(frame, "Login", attempt_login).pack(pady=15)
        self.app_button(frame, "Back", self.build_user_select).pack(pady=10)


    # Company main dashboard

    def build_company_main(self):
        """
        Main company dashboard with all possible actions.
        """
        self.clear()
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, padx=20, pady=50)

        tk.Label(frame, text="Company Dashboard", font=("Helvetica", 20, "bold"),
                 bg="#2c2c2c", fg="white").pack(pady=20)

        self.app_button(frame, "View Inventory", self.build_company_inventory).pack(pady=10)
        self.app_button(frame, "View Sales Summary", self.build_sales_summary).pack(pady=10)
        self.app_button(frame, "View Expense Pie Chart", self.build_company_expenses_chart).pack(pady=10)
        self.app_button(frame, "Add New Product", self.build_add_product_page).pack(pady=10)
        self.app_button(frame, "Finish Session", self.build_user_select).pack(pady=10)


    # Add new product page

    def build_add_product_page(self):
        """
        Add product page.
        Using a frame for entries and a separate frame for buttons to avoid pack/grid conflict.
        """
        self.clear()
        tk.Label(self.root, text="Add New Product", font=("Arial", 18), bg="#2c2c2c", fg="white").pack(pady=15)

        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(pady=10, padx=20)

        labels = ["Name:", "Cost:", "Price:", "Manufacturer:", "Initial Stock:"]
        entries = []

        for i, text in enumerate(labels):
            tk.Label(frame, text=text, bg="#2c2c2c", fg="white").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        def submit():
            """
            Convert inputs and add product to inventory.
            Syncs company data.
            """
            try:
                name = entries[0].get().strip()
                cost = float(entries[1].get())
                price = float(entries[2].get())
                manu = entries[3].get().strip()
                stock = int(entries[4].get())

                if not name or not manu:
                    raise ValueError("Name and Manufacturer cannot be empty.")

                new_product = self.inventory.add_product(name, cost, price, manu, stock)

                self.company.products = self.inventory.products
                self.company.total_earnings = self.inventory.total_earnings

                messagebox.showinfo("Success",
                                    f"Product added!\nUPC: {new_product.code}\nName: {new_product.product_name}")
                self.build_company_main()

            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        # separate frame for buttons to avoid pack/grid conflict
        btn_frame = tk.Frame(self.root, bg="#2c2c2c")
        btn_frame.pack(pady=15)
        self.app_button(btn_frame, "Add Product", submit).pack(side="left", padx=10)
        self.app_button(btn_frame, "Back", self.build_company_main).pack(side="left", padx=10)


    # Company inventory

    def build_company_inventory(self):
        """
        Show a Listbox of all products and stock levels.
        We could improve with a Treeview for sorting/filtering.
        """
        self.clear()
        tk.Label(self.root, text="Inventory Overview", font=("Arial", 18), bg="#2c2c2c", fg="white").pack(pady=10)

        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        box = tk.Listbox(frame, width=80, height=max(len(self.inventory.products), 10),
                         font=("Arial", 12),
                         yscrollcommand=scrollbar.set,
                         bg="#1c1c1c", fg="white",
                         selectbackground="#8B0000")
        box.pack(side="left", fill="both", expand=True, pady=10)
        scrollbar.config(command=box.yview)

        for p in self.inventory.products:
            line = f"{p.product_name} | ${p.selling_price:.2f} | Stock: {p.stock}"
            box.insert(tk.END, line)

        self.app_button(self.root, "Back", self.build_company_main).pack(pady=10)


    # Sales summary

    def build_sales_summary(self):
        self.clear()
        tk.Label(self.root, text="Sales Summary", font=("Arial", 18), fg="white", bg="#1c1c1c").pack(pady=10)
        tk.Label(self.root, text=f"Total Earnings: ${self.inventory.total_earnings:.2f}",
                 font=("Arial", 14), fg="white", bg="#1c1c1c").pack(pady=5)
        self.app_button(self.root, "Back", self.build_company_main).pack(pady=20)


    # expense pie chart

    def build_company_expenses_chart(self):
        """
        Shows a pie chart for company expense breakdown.
        Using matplotlib + Tkinter canvas. Could make interactive later.
        """
        self.clear()
        tk.Label(self.root, text="Expense Distribution", font=("Arial", 18), fg="white", bg="#1c1c1c").pack(pady=10)

        self.company.products = self.inventory.products
        self.company.total_earnings = self.inventory.total_earnings

        percentages = self.company.percentages()
        labels = list(percentages.keys())
        values = list(percentages.values())

        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("Company Expense Breakdown")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)

        self.app_button(self.root, "Back", self.build_company_main).pack(pady=10)


    # Customer main page
    def build_customer_main(self):
        self.clear()
        tk.Label(self.root, text="Welcome, Customer!", font=("Arial", 16),
                 fg="white", bg="#1c1c1c").pack(pady=10)

        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(pady=10, padx=20)

        tk.Label(frame, text="Available Products:", bg="#2c2c2c", fg="white",
                 font=("Arial", 14)).pack(pady=5)

        # --- Listbox + scrollbar ---
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.product_list = tk.Listbox(
            frame,
            width=80,
            height=12,
            bg="#1c1c1c",
            fg="white",
            selectbackground="#8B0000",
            yscrollcommand=scrollbar.set,
            font=("Arial", 12)
        )
        self.product_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.product_list.yview)

        # Populate listbox (old logic)
        self.product_list.delete(0, tk.END)
        for p in self.inventory.products:
            line = f"{p.code} | {p.product_name} - ${p.selling_price:.2f} | Stock: {p.stock}"
            self.product_list.insert(tk.END, line)

        tk.Button(frame, text="Add to Cart", command=self.add_to_cart,
                  bg="#8B0000", fg="white", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="View Cart / Checkout",
                  width=20, bg="#8B0000", fg="white",
                  command=self.build_cart_page).pack(pady=5)

        tk.Button(self.root, text="Back", width=20,
                  bg="#8B0000", fg="white",
                  command=self.build_user_select).pack(pady=5)

    def add_to_cart(self):
        selection = self.product_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a product.")
            return

        product = self.inventory.products[selection[0]]

        if product.stock <= 0:
            messagebox.showerror("Out of Stock", f"{product.product_name} is unavailable.")
            return

        # OLD LOGIC — do NOT modify stock now
        self.cart.append(product)

        messagebox.showinfo("Added", f"{product.product_name} added to cart!")
        self.build_customer_main()

    def build_cart_page(self):
        self.clear()

        tk.Label(self.root, text="Your Cart", font=("Arial", 16),
                 fg="white", bg="#1c1c1c").pack(pady=10)

        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(pady=10, padx=20)

        cart_box = tk.Listbox(
            frame, width=60, height=10,
            bg="#1c1c1c", fg="white",
            selectbackground="#8B0000",
            font=("Arial", 12)
        )
        cart_box.pack()

        total_price = 0
        for p in self.cart:
            cart_box.insert(tk.END, f"{p.product_name} - ${p.selling_price:.2f}")
            total_price += p.selling_price

        tk.Label(self.root, text=f"Total: ${total_price:.2f}",
                 font=("Arial", 14), fg="white", bg="#1c1c1c").pack(pady=10)

        tk.Button(self.root, text="Confirm Purchase",
                  bg="#8B0000", fg="white",
                  command=lambda: self.checkout(total_price)).pack(pady=10)

        tk.Button(self.root, text="Back",
                  bg="#8B0000", fg="white",
                  command=self.build_customer_main).pack(pady=10)

    def checkout(self, total):
        messagebox.showinfo("Thank you!", f"Purchase complete!\nTotal: ${total:.2f}")

        # OLD LOGIC — stock reduced after purchase
        for p in self.cart:
            p.stock -= 1

        self.inventory.total_earnings += total
        self.cart = []

        self.build_customer_main()

    # def build_customer_main(self):
    #     self.clear()
    #     tk.Label(self.root, text="Welcome, Customer!", font=("Arial", 16), fg="white", bg="#1c1c1c").pack(pady=10)
    #
    #     frame = tk.Frame(self.root, bg="#2c2c2c")
    #     frame.pack(pady=10, padx=20)
    #
    #     tk.Label(frame, text="Available Products:", bg="#2c2c2c", fg="white", font=("Arial", 14)).pack(pady=5)
    #
    #     # --- Listbox + scrollbar ---
    #     scrollbar = tk.Scrollbar(frame)
    #     scrollbar.pack(side="right", fill="y")
    #
    #     self.product_list = tk.Listbox(frame, width=80, height=len(self.inventory.products),
    #                                    bg="#1c1c1c", fg="white",
    #                                    selectbackground="#8B0000",
    #                                    yscrollcommand=scrollbar.set,
    #                                    font=("Arial", 12))
    #     self.product_list.pack(side="left", fill="both", expand=True)
    #     scrollbar.config(command=self.product_list.yview)
    #
    #     # populate listbox
    #     for p in self.inventory.products:
    #         line = f"{p.code} | {p.product_name} - ${p.selling_price:.2f} | Stock: {p.stock}"
    #         self.product_list.insert(tk.END, line)
    #     # note: rebuild every time page is loaded to reflect stock changes
    #     # alternative: only update changed products for efficiency
    #
    #     self.app_button(frame, "Add to Cart", self.add_to_cart).pack(pady=10)
    #     self.app_button(self.root, "View Cart / Checkout", self.build_cart_page).pack(pady=5)
    #     self.app_button(self.root, "Back", self.build_user_select).pack(pady=5)
    #
    #
    # # Add to cart
    #
    # def add_to_cart(self):
    #     selection = self.product_list.curselection()
    #     if not selection:
    #         messagebox.showwarning("No selection", "Please select a product.")
    #         return
    #
    #     index = selection[0]
    #     product = self.inventory.products[index]
    #
    #     # check if already in cart
    #     for item in self.cart:
    #         if item["product"] == product:
    #             item["quantity"] += 1
    #             product.update_stock(1)
    #             messagebox.showinfo("Added", f"{product.product_name} quantity increased in cart!")
    #             self.build_customer_main()
    #             return
    #
    #     self.cart.append({"product": product, "quantity": 1})
    #     product.update_stock(1)
    #     messagebox.showinfo("Added", f"{product.product_name} added to cart!")
    #     self.build_customer_main()
    #
    #
    # # Cart page
    #
    # def build_cart_page(self):
    #     """
    #     Shows cart items with quantity controls and total price.
    #     Could later add remove-all button, discounts, etc.
    #     """
    #     self.clear()
    #     tk.Label(self.root, text="Your Cart", font=("Arial", 16), fg="white", bg="#1c1c1c").pack(pady=10)
    #
    #     frame = tk.Frame(self.root, bg="#2c2c2c")
    #     frame.pack(fill="both", expand=True, pady=10, padx=20)
    #
    #     total_price = 0
    #     for idx, item in enumerate(self.cart):
    #         product = item["product"]
    #         quantity = item["quantity"]
    #
    #         tk.Label(frame, text=f"{product.product_name} ${product.selling_price:.2f}", width=40,
    #                  anchor="w", bg="#2c2c2c", fg="white", font=("Arial", 12)).grid(row=idx, column=0, pady=5)
    #         tk.Label(frame, text=f"Quantity: {quantity}", width=15, bg="#2c2c2c", fg="white", font=("Arial", 12)).grid(
    #             row=idx, column=1)
    #
    #         tk.Button(frame, text="+", width=3, font=("Arial", 12),
    #                   command=lambda i=idx: self.change_quantity(i, 1), bg="#8B0000", fg="white").grid(row=idx,
    #                                                                                                    column=2, padx=5)
    #         tk.Button(frame, text="-", width=3, font=("Arial", 12),
    #                   command=lambda i=idx: self.change_quantity(i, -1), bg="#8B0000", fg="white").grid(row=idx,
    #                                                                                                     column=3,
    #                                                                                                     padx=5)
    #
    #         total_price += product.selling_price * quantity
    #
    #     tk.Label(self.root, text=f"Total: ${total_price:.2f}", font=("Arial", 14), fg="white", bg="#1c1c1c").pack(
    #         pady=10)
    #
    #     tk.Button(self.root, text="Confirm Purchase", command=lambda: self.checkout(total_price)).pack(pady=5)
    #     tk.Button(self.root, text="Back", command=self.build_customer_main).pack(pady=5)
    #
    #
    # # Change quantity helper
    #
    # def change_quantity(self, idx, delta):
    #     """
    #     Adjust quantity in cart by delta (+1 or -1).
    #     Remove item if quantity hits 0.
    #     """
    #     item = self.cart[idx]
    #     if delta > 0:
    #         if item["product"].stock <= 0:
    #             messagebox.showerror("Stock", "No more stock.")
    #             return
    #         item["quantity"] += 1
    #         item["product"].update_stock(1)
    #     else:
    #         item["quantity"] -= 1
    #         item["product"].stock += 1
    #         if item["quantity"] == 0:
    #             self.cart.pop(idx)
    #     self.build_cart_page()  # refresh page to reflect new quantity
    #
    #
    # # Checkout
    #
    # def checkout(self, total):
    #     """
    #     Confirm purchase, add to earnings, clear cart.
    #     """
    #     messagebox.showinfo("Thank you!", f"Purchase complete!\nTotal: ${total:.2f}")
    #     self.inventory.total_earnings += total
    #     self.cart = []
    #     self.build_customer_main()
    #

    # Utility: clear screen

    def clear(self):
        """
        Remove all widgets from root.
        Simple way to "switch pages".
        """
        for widget in self.root.winfo_children():
            widget.destroy()



# Run App
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1c1c1c")
    root.resizable(True, True)
    root.state("zoomed")
    app = ShoppingApp(root)
    root.mainloop()
