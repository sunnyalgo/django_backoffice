from unittest.mock import patch

import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_ordered_product_total_price(ordered_products, all_prices):
    for position, ordered_product in enumerate(ordered_products):
        assert ordered_product.total_price() == all_prices[position]


@pytest.mark.django_db
def test_ordered_product_total_weight(ordered_products, all_weights):
    for position, ordered_product in enumerate(ordered_products):
        assert ordered_product.total_weight() == all_weights[position]


@pytest.mark.django_db
def test_ordered_product_total_seller_commission(ordered_products, all_seller_commissions):
    for position, ordered_product in enumerate(ordered_products):
        assert ordered_product.total_seller_commission() == all_seller_commissions[position]


@pytest.mark.django_db
def test_order_total_price(order, ordered_products, order_total_price):
    assert order.order_total_price() == order_total_price


@pytest.mark.django_db
def test_order_total_weight(order, ordered_products, order_total_weight):
    assert order.order_total_weight() == order_total_weight


@pytest.mark.django_db
def test_order_total_seller_commission(order, ordered_products, order_total_seller_commission):
    assert order.order_total_seller_commission() == order_total_seller_commission
