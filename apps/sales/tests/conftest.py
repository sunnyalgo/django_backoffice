import pytest
from model_bakery import baker


@pytest.fixture
def order():
    return baker.make("Order")


@pytest.fixture
def avaliable_products():
    return (baker.make("Product", name='book',
                       weight=0.8, price=5.99, seller_commission_tax=0.5),
            baker.make("Product", name='snow ski',
                       weight=3.5, price=599.99, seller_commission_tax=15),
            baker.make("Product", name='new membership',
                       weight=0, price=29.99, seller_commission_tax=0))


@pytest.fixture
def ordered_products(order, avaliable_products):
    return (baker.make("OrderedProduct", product=avaliable_products[0], quantity=3, order=order),
            baker.make("OrderedProduct", product=avaliable_products[1], quantity=2, order=order),
            baker.make("OrderedProduct", product=avaliable_products[2], quantity=1, order=order))


@pytest.fixture
def all_prices():
    return ((5.99 * 3),
            (599.99 * 2),
            (29.99 * 1))


@pytest.fixture
def order_total_price():
    return 1247.94


@pytest.fixture
def all_weights():
    return ((0.8 * 3),
            (3.5 * 2),
            (0 * 1))


@pytest.fixture
def order_total_weight():
    return 9.4


@pytest.fixture
def all_seller_commissions():
    return ((5.99 * 3 * 0.005),
            (599.99 * 2 * 0.15),
            (29.99 * 1 * 0))


@pytest.fixture
def order_total_seller_commission():
    return 180.08685
