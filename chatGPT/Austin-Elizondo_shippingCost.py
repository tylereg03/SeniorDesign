def calculate_shipping_cost(weight, distance):
    """Calculate the shipping cost."""
    if weight <= 5:
        return weight * 2 * distance
    elif weight > 5 and weight <= 20:
        return weight * 3 * distance
    elif weight > 20 and weight <= 50:
        return weight * 5 * distance
    else:
        return weight * 7 * distance

def calculate_tax(price, tax_rate):
    """Calculate the tax."""
    return price * tax_rate

def calculate_total_cost(price, weight, distance, tax_rate):
    """Calculate the total cost."""
    shipping_cost = calculate_shipping_cost(weight, distance)
    tax_amount = calculate_tax(price, tax_rate)
    return price + shipping_cost + tax_amount
