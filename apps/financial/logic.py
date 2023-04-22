from functools import lru_cache
from utils.django_models.dynamic_import import get_model_class


@lru_cache(maxsize=1)
def get_cached_product_type(product_type_name):
    ProductType = get_model_class('product.ProductType')
    return ProductType.objects.get(name=product_type_name)


def calculate_royalties_gross_price(order_model):
    product_type = get_cached_product_type('Physical Book')
    product_details = order_model.ordered_products.filter(
        product__product_type=product_type.id).values('quantity', 'product__price')
    total_royalties_gross_price = 0
    for product_details in product_details:
        total_royalties_gross_price += product_details['product__price'] * product_details['quantity']
    return total_royalties_gross_price
