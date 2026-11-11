def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order

def bill(items, gst_rate=0.05):
    subtotal = sum(items)
    gst = subtotal * gst_rate
    return subtotal, gst, subtotal + gst

if __name__ == "__main__":
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))
    print(bill([30, 20]))
    print(add_item_buggy.__defaults__)
