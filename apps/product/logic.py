from django.utils import timezone


def define_sku_code(product_type_name):
    prefix = '-'.join([initials.upper()[:3] for initials in product_type_name.split(' ')[:2]])
    code = timezone.now().strftime('%y%m%d-%H%M%S-%f')[:19]
    return f'{prefix}-{code}'
