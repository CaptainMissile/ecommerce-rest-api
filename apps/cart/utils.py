from apps.products.models import ProductInventory

def check_existence_in_cart(data, cart_items):
        for item in cart_items:
            if data['product'] == item.product.id:
                return {'does_exist' :True, 'item':item}
        
        return{'does_exist' : False, 'item': None}


def quantity_lt_remaining_units(data):
    product = ProductInventory.objects.filter(id = data['product'])

    if product.exists() and int(data['quantity']) <= product[0].units:
        return True
    else:
        return False