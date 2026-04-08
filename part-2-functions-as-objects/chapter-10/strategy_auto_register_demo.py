"""
Demo for 03-strategy-auto-registration-with-decorator.md (Fluent Python 10.3).

Implements an order discount system where:
- promotions register themselves via @promotion at import time
- best_promo never needs manual list maintenance
- optional group registration via @promotion_group("name")
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import NamedTuple


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: Sequence[LineItem]

    def total(self) -> Decimal:
        return sum((item.total() for item in self.cart), start=Decimal(0))


Promotion = Callable[[Order], Decimal]

promos: list[Promotion] = []


def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    return max((promo(order) for promo in promos), default=Decimal(0))


@promotion
def fidelity(order: Order) -> Decimal:
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal("0.05")
    return Decimal(0)


@promotion
def bulk_item(order: Order) -> Decimal:
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal("0.10")
    return discount


@promotion
def large_order(order: Order) -> Decimal:
    distinct = {item.product for item in order.cart}
    if len(distinct) >= 10:
        return order.total() * Decimal("0.07")
    return Decimal(0)


# --- Optional: grouped registration (parameterized decorator) -----------------

groups: dict[str, list[Promotion]] = defaultdict(list)


def promotion_group(group: str = "default"):
    def decorate(promo: Promotion) -> Promotion:
        groups[group].append(promo)
        return promo

    return decorate


def best_group_promo(order: Order, group: str) -> Decimal:
    return max((promo(order) for promo in groups.get(group, [])), default=Decimal(0))


@promotion_group("vip")
def vip_extra(order: Order) -> Decimal:
    if order.customer.fidelity >= 2000:
        return order.total() * Decimal("0.02")
    return Decimal(0)


def money(x: str) -> Decimal:
    return Decimal(x)


def main() -> None:
    ann = Customer("Ann", 1100)
    vip = Customer("VIP", 2500)
    cart = [
        LineItem("banana", 30, money("0.50")),
        LineItem("apple", 10, money("1.50")),
    ]
    order = Order(ann, cart)
    order_vip = Order(vip, cart)

    print("registered promos ->", [p.__name__ for p in promos])
    print("best_promo discount ->", best_promo(order))
    print("due ->", order.total() - best_promo(order))

    print("\nregistered groups ->", {k: [p.__name__ for p in v] for k, v in groups.items()})
    print("best_group_promo('vip') on ann ->", best_group_promo(order, "vip"))
    print("best_group_promo('vip') on vip ->", best_group_promo(order_vip, "vip"))


if __name__ == "__main__":
    main()

