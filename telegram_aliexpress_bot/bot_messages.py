# todo: Unit tests


def get_product_promotion_message(product_title, product_price, product_url):
    message = '{0}\n{1}\n\n{2}'.format(product_title, product_price, product_url)
    return message
