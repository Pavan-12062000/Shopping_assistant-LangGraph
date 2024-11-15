# 

import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional, Union, List, Dict, Tuple
import json

def load_products_from_json() -> List[Dict]:
    """
    Load products from a JSON file.

    Returns:
        List[Dict]: A list of product dictionaries loaded from the JSON file.
    """
    try:
        with open('products.json', 'r') as file:
            products = json.load(file)
        return products
    except Exception as e:
        return f"Error loading products: {e}"
        return []

def search_products(
    description: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    quantity: Optional[int] = None,
) -> List[Dict]:
    """
    Search for products based on description, price, quantity.

    Args:
        description: The name or part of the name of the product. Defaults to None.
        min_price: The minimum price. Defaults to None.
        max_price: The maximum price. Defaults to None.
        quantity: The quantity available. Defaults to None.

    Returns:
        List[Dict]: A list of product dictionaries matching the search criteria.
    """
    # Load products from the JSON file
    products = load_products_from_json()

    # Filter products based on the search criteria
    filtered_products = []
    for product in products:
        if description and description.lower() not in product['Description'].lower():
            continue
        if min_price is not None and product['UnitPrice'] < min_price:
            continue
        if max_price is not None and product['UnitPrice'] > max_price:
            continue
        if quantity is not None and product['Quantity'] < quantity:
            continue
        
        # If it passed all filters, add it to the results
        filtered_products.append(product)

    # Limit to 2 products for now, as per original logic
    return json.dumps(filtered_products[:2])

cart = {}  # This is a global cart that persists throughout the session.

def add_to_cart(product_data, quantity):
    """
    Add a product to the cart.
    
    :param product_data: dict with keys 'StockCode', 'Description', 'Quantity', 'UnitPrice'
    :param quantity: int, number of items to add
    """
    stock_code = product_data["StockCode"]
    if stock_code in cart:
        # Update the quantity if the product is already in the cart
        cart[stock_code]["Quantity"] += quantity
    else:
        # Add a new entry to the cart
        cart[stock_code] = {
            "Description": product_data["Description"],
            "UnitPrice": product_data["UnitPrice"],
            "Quantity": quantity
        }
    return f"Added {quantity} of {product_data['Description']} to cart."

def remove_from_cart(stock_code, quantity):
    """
    Remove a specified quantity of a product from the cart.
    
    :param stock_code: str, unique identifier for the product
    :param quantity: int, number of items to remove
    """
    if stock_code in cart:
        if cart[stock_code]["Quantity"] > quantity:
            # Reduce quantity if more items are in the cart
            cart[stock_code]["Quantity"] -= quantity
            return f"Removed {quantity} of {cart[stock_code]['Description']} from cart."
        elif cart[stock_code]["Quantity"] == quantity:
            # Remove the item entirely if quantities match
            del cart[stock_code]
            return f"Removed {cart[stock_code]['Description']} from cart."
        else:
            return f"Cannot remove {quantity}; only {cart[stock_code]['Quantity']} available."
    else:
        return "Item not found in cart."

def view_cart():
    """
    Display the contents of the cart.
    """
    cart1 = ""
    cart2 = ""
    if not cart:
        return "Cart is empty."
    else:
        cart1 += "Your cart contains:"
        for stock_code, item in cart.items():
            cart2 += f"{item['Description']}: {item['Quantity']} @ ${item['UnitPrice']} each"
    return cart1+cart2


# In tools.py
def checkout(cart, user_confirmed=False):
    """
    Initiates the checkout process. Prompts for user confirmation.
    """
    if not cart:
        return "Your cart is empty. Please add some items before proceeding to checkout."

    total_price = sum(item["UnitPrice"] * item["Quantity"] for item in cart)
    
    # If user has not confirmed, prompt for confirmation
    if not user_confirmed:
        return f"Checkout initiated. The total price is ${total_price:.2f}. Do you want to proceed with the payment? (yes/no)"
    
    # Proceed with checkout if confirmation is received
    return f"Confirmed! Processing payment for ${total_price:.2f}."


def payment_options():
    """
    Returns the available payment options.
    """
    return "We accept the following payment methods: Credit/Debit cards, PayPal, Bank Transfer."

def thank_you():
    """
    Returns a thank you message after the payment option.
    """
    return "Thank you for shopping with us!"

def estimated_delivery_time(country="Canada"):
    """
    Returns the estimated delivery time based on the country.
    """
    delivery_times = {
        "UK": "2-3 business days",
        "US": "5-7 business days",
        "Canada": "5-7 business days",
        "Australia": "7-10 business days",
    }
    
    return f"Estimated delivery time to {country}: {delivery_times.get(country, '7-10 business days')}"


order_statuses = {
    "1": "Order placed, awaiting processing.",
    "2": "Order packed.",
    "3": "Order in Progress.",
    "4": "Order arrived to nearest hub.",
    "5": "Out for delivery.",
    "6": "Order delivered.",
}

def order_status(order_id):
    """
    Returns the current status of an order.
    """

    return order_statuses.get(order_id, "Order ID not found.")