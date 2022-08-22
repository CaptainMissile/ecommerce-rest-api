


def check_existence(data, cart_items):
        for item in cart_items:
            if data['product'] == item.product.id:
                return {'does_exist' :True, 'item':item}
        
        return{'does_exist' : False, 'item': None}


def units_gt_quantity(data, item):
    if data['quantity'] <= item.units:
        return True