def text_to_price(text):
    return int(text.replace('$', '').replace(',', '').replace('.', ''))
