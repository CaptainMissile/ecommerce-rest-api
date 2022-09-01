def calc_price(item, product_inventory):
    print(item.quantity)
    return item.quantity * product_inventory.price

def cart_quantity_lt_remaining_units(cart_data, product_inventory):
    if cart_data.quantity > 0 and product_inventory is not None and cart_data.quantity <= product_inventory.units:
        return True
    
    return False

