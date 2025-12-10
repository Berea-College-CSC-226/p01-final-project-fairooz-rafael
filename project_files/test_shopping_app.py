######################################################################
# Author: Rafael, Fairooz
# Username: hermozafreitasr, tasniaf
#
# Purpose: sociated with a unique product in an inventory store
#
######################################################################
# Acknowledgements:
#
# None: Original work

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import pytest
from inventory import Inventory
from product import Product
from graphics_interface_for_company import CompanyExpenses
from interating_new_features import ShoppingApp
import tkinter as tk


# ============================================================
#   INVENTORY TESTS
# ============================================================

def test_inventory_initial_load():
    inv = Inventory()
    assert isinstance(inv.products, list)
    assert all(isinstance(p, Product) for p in inv.products)


def test_add_product_success():
    inv = Inventory()
    n_before = len(inv.products)

    new_p = inv.add_product(
        name="Test Item",
        cost=2.50,
        price=4.99,
        manu="Tester",
        stock=10
    )

    assert len(inv.products) == n_before + 1
    assert isinstance(new_p, Product)
    assert new_p.product_name == "Test Item"
    assert new_p.selling_price == 4.99
    assert new_p.stock == 10
    assert new_p.code is not None   # UPC auto-generated


def test_add_product_invalid_values():
    inv = Inventory()

    with pytest.raises(ValueError):
        inv.add_product("", 1.0, 1.0, "X", 5)

    with pytest.raises(ValueError):
        inv.add_product("Valid", -1.0, 1.0, "X", 5)

    with pytest.raises(ValueError):
        inv.add_product("Valid", 1.0, 1.0, "", 5)

    with pytest.raises(ValueError):
        inv.add_product("Valid", 1.0, 1.0, "X", -5)


# ============================================================
#   COMPANY EXPENSES TESTS
# ============================================================

def test_company_expenses_consistency():
    inv = Inventory()
    comp = CompanyExpenses()

    comp.products = inv.products
    comp.total_earnings = 200.0

    result = comp.percentages()

    assert "Original Cost" in result
    assert "Revenue" in result
    assert "Profit" in result

    # Percentages add to ~100
    total = sum(result.values())
    assert 98 <= total <= 102


# ============================================================
#   SHOPPING APP (LOGIC ONLY) TESTS
# ============================================================

def test_cart_addition_and_checkout():
    root = tk.Tk()               # GUI required for instantiation
    app = ShoppingApp(root)

    product = app.inventory.products[0]
    initial_stock = product.stock

    app.cart.append(product)
    app.checkout(product.selling_price)

    assert product.stock == initial_stock - 1
    assert len(app.cart) == 0
    assert app.inventory.total_earnings >= product.selling_price


def test_sync_company_inventory_after_add():
    root = tk.Tk()
    app = ShoppingApp(root)

    before = len(app.company.products)

    # Add a product
    new_p = app.inventory.add_product(
        "SyncTest",
        1.0,
        3.0,
        "Sync",
        5
    )

    # Update sync
    app.company.products = app.inventory.products

    assert len(app.company.products) == before + 1
    assert new_p in app.company.products
