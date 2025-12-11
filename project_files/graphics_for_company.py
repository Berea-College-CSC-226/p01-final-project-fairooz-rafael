######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: draw a pie graph chart using preloaded data, providing statistics to the company
#
######################################################################
# Acknowledgements:
#
# None, but using graphics_interface_for_company as reference

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graphics_interface_for_company import *


class CompanyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Company Expense Percentages")

        self.company = CompanyExpenses(rent=800, salaries=1200, other=200)

        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        ttk.Button(frame, text="Show Expense Pie Chart",
                   command=self.show_pie_chart).pack(pady=10)

        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack()

    def show_pie_chart(self):
        #clear old chart if it exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        percentages = self.company.percentages()

        labels = list(percentages.keys())
        values = list(percentages.values())

        #create matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("Company Expense Distribution")

        #embed graph inside Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        plt.close(fig)   # prevents duplicate external windows



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x650")
    app = CompanyGUI(root)
    root.mainloop()