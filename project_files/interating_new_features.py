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
        self.root.configure(bg="#1c1c1c")
        self.root.resizable(True, True)

        self.inventory = Inventory()
        self.company = CompanyExpenses()   # <-- Uses same file-based product loading

        # Sync inventory into company tracker:
        self.company.products = self.inventory.products

        self.cart = []

        self.build_user_select()

    def app_button(self, master, text, command):

        return tk.Button(master, text=text, width=25, height=2,
                         bg="#8B0000", fg="white", font=("Helvetica", 12, "bold"),
                         activebackground="#A52A2A", activeforeground="white",
                         command=command)

    # -----------------------------
    # Page 1 — User Type Selection
    # -----------------------------
    def build_user_select(self):
        self.clear()

        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, padx=20, pady=50)

        tk.Label(frame, text="Select User Type",
                 font=("Helvetica", 24, "bold"),
                 bg="#2c2c2c", fg="white").pack(pady=30)

        self.app_button(frame, "Customer", self.build_customer_main).pack(pady=15)
        self.app_button(frame, "Company", self.build_company_login).pack(pady=15)


    # -----------------------------
    # Company Login
    # -----------------------------
    def build_company_login(self):
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
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username == "admin" and password == "1234":
                messagebox.showinfo("Welcome", "Login successful.")
                self.build_company_main()
            else:
                messagebox.showerror("Access Denied", "Incorrect credentials.")

        self.app_button(frame, "Login", attempt_login).pack(pady=15)
        self.app_button(frame, "Back", self.build_user_select).pack(pady=10)


    # -----------------------------
    # Company Dashboard
    # -----------------------------
    def build_company_main(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, padx=20, pady=50)

        tk.Label(frame, text="Company Dashboard", font=("Helvetica", 20, "bold"),
                 bg="#2c2c2c", fg="white").pack(pady=20)

        self.app_button(frame, "View Inventory", self.build_company_inventory).pack(pady=10)
        self.app_button(frame, "View Sales Summary", self.build_sales_summary).pack(pady=10)
        self.app_button(frame, "View Expense Pie Chart", self.build_company_expenses_chart).pack(pady=10)
        self.app_button(frame, "Finish Session", self.build_user_select).pack(pady=10)

    # -----------------------------
    # Inventory view
    # -----------------------------
    def build_company_inventory(self):
        self.clear()
        tk.Label(self.root, text="Inventory Overview", font=("Arial", 18),bg="#2c2c2c", fg="white").pack(pady=10)

        frame = tk.Frame(self.root, bg="#2c2c2c")  # dark background frame
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side="right", fill="y", pady=10)

        box = tk.Listbox(self.root,
                         width=80, height=max(len(self.inventory.products), 10),
                         font=("Arial", 12),
                         yscrollcommand=scrollbar.set,
                         bg="#1c1c1c", fg="white", selectbackground="#8B0000")

        box.pack(side="left", fill="both", expand=True, pady=10)

        scrollbar.config(command=box.yview)

        for p in self.inventory.products:
            line = f"{p.product_name} | ${p.selling_price:.2f} | Stock: {p.stock}"
            box.insert(tk.END, line)

        self.app_button(self.root, "Back", self.build_company_main).pack(pady=10)


    # -----------------------------
    # Sales Summary
    # -----------------------------
    def build_sales_summary(self):
        self.clear()
        tk.Label(self.root, text="Sales Summary", font=("Arial", 18), fg="white", bg="#1c1c1c").pack(pady=10)

        tk.Label(self.root, text=f"Total Earnings: ${self.inventory.total_earnings:.2f}",
                 font=("Arial", 14),fg="white", bg="#1c1c1c").pack(pady=5)

        self.app_button(self.root, "Back", self.build_company_main).pack(pady=20)

    # -----------------------------
    # NEW: Expense Pie Chart
    # -----------------------------
    def build_company_expenses_chart(self):
        self.clear()

        tk.Label(self.root, text="Expense Distribution", font=("Arial", 18),fg="white", bg="#1c1c1c").pack(pady=10)

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

        self.app_button(self.root, "Back", self.build_company_main).pack(pady=10)

    # -----------------------------
    # Customer Shopping
    # -----------------------------
    def build_customer_main(self):
        self.clear()

        tk.Label(self.root, text="Welcome, Customer!", font=("Arial", 16),fg="white", bg="#1c1c1c").pack(pady=10)

        frame = tk.Frame(self.root, bg= "#2c2c2c")
        frame.pack(pady=10, padx=20)

        tk.Label(frame, text="Available Products:", bg="#2c2c2c", fg="white", font=("Arial", 14)).pack(pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.product_list = tk.Listbox(frame, width=80, height=len(self.inventory.products),
                                       bg="#1c1c1c", fg="white",
                                       selectbackground="#8B0000",
                                       yscrollcommand=scrollbar.set,
                                       font=("Arial", 12))
        self.product_list.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.product_list.yview)

        for p in self.inventory.products:
            line = (
                f"{p.code} | {p.product_name} - ${p.selling_price:.2f} "
                f"| Stock: {p.stock}"
            )
            self.product_list.insert(tk.END, line)

        self.app_button(frame, "Add to Cart", self.add_to_cart).pack(pady=10)
        self.app_button(self.root, "View Cart / Checkout", self.build_cart_page).pack(pady=5)
        self.app_button(self.root, "Back", self.build_user_select).pack(pady=5)

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

        for item in self.cart:
            if item["product"] == product:
                item["quantity"] += 1
                product.update_stock(1)
                messagebox.showinfo("Added", f"{product.product_name} quantity increased in cart!")
                self.build_customer_main()
                return


        self.cart.append({"product": product, "quantity": 1})
        product.update_stock(1)
        messagebox.showinfo("Added", f"{product.product_name} added to cart!")
        self.build_customer_main()


    # -----------------------------
    # Cart Page
    # -----------------------------
    def build_cart_page(self):
        self.clear()

        tk.Label(self.root, text="Your Cart", font=("Arial", 16),fg="white", bg="#1c1c1c").pack(pady=10)

        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(fill="both", expand=True, pady=10, padx=20)

        total_price = 0

        for idx, item in enumerate(self.cart):
            product = item["product"]
            quantity = item["quantity"]

            tk.Label(frame, text=f"{product.product_name} ${product.selling_price:.2f}", width=40,
                     anchor="w", bg="#2c2c2c", fg="white", font=("Arial", 12)).grid(row=idx, column=0, pady=5)
            tk.Label(frame, text=f"Quantity: {quantity}", width=15, bg="#2c2c2c", fg="white", font=("Arial", 12)).grid(row=idx, column=1)

            tk.Button(frame, text="+", width=3, font=("Arial", 12),
                      command=lambda i=idx: self.change_quantity(i, 1), bg="#8B0000", fg="white").grid(row=idx,column=2, padx=5)
            tk.Button(frame, text="-", width=3, font=("Arial", 12),
                      command=lambda i=idx: self.change_quantity(i, -1), bg="#8B0000", fg="white").grid(row=idx,column=3,padx=5)

        total_price += product.selling_price * quantity

        tk.Label(self.root, text=f"Total: ${total_price:.2f}", font=("Arial", 14),fg="white", bg="#1c1c1c").pack(pady=10)


        tk.Button(self.root, text="Confirm Purchase",
                  command=lambda: self.checkout(total_price)).pack(pady=5)
        tk.Button(self.root, text="Back",
                  command=self.build_customer_main).pack(pady=5)

    # -----------------------------
    # Helper to change quantity
    # -----------------------------
    def change_quantity(self, idx, delta):
        item = self.cart[idx]
        if delta > 0:
            if item["product"].stock <= 0:
                messagebox.showerror("Stock", "No more stock.")
                return
            item["quantity"] += 1
            item["product"].update_stock(1)
        else:
            item["quantity"] -= 1
            item["product"].stock += 1
            if item["quantity"] == 0:
                self.cart.pop(idx)
        self.build_cart_page()


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
    root.configure(bg="#1c1c1c")  # Dark background
    root.resizable(True, True)
    root.state("zoomed")
    app = ShoppingApp(root)
    root.mainloop()
