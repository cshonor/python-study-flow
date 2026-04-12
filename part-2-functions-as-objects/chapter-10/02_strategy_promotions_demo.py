"""
Demo for 02-10.2 策略模式：从“类层级”到“一等函数”重构.md (Fluent Python 10.2).

Shows:
- classic Strategy pattern with classes (Promotion ABC)
- functional Strategy: promotion as a function
- best_promo with manual list
- auto collection via decorator registration
"""

from __future__ import annotations

from abc import ABC, abstractmethod
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


# --- Classic (class-based) strategy ------------------------------------------


class Promotion(ABC):
    @abstractmethod
    def discount(self, order: "OrderClassic") -> Decimal: ...


@dataclass(frozen=True)
class OrderClassic:
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Promotion | None = None

    def total(self) -> Decimal:
        return sum((item.total() for item in self.cart), start=Decimal(0))

    def due(self) -> Decimal:
        discount = Decimal(0) if self.promotion is None else self.promotion.discount(self)
        return self.total() - discount


class FidelityPromo(Promotion):
    def discount(self, order: OrderClassic) -> Decimal:
        if order.customer.fidelity >= 1000:
            return order.total() * Decimal("0.05")
        return Decimal(0)


class BulkItemPromo(Promotion):
    def discount(self, order: OrderClassic) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal("0.10")
        return discount


class LargeOrderPromo(Promotion):
    def discount(self, order: OrderClassic) -> Decimal:
        distinct = {item.product for item in order.cart}
        if len(distinct) >= 10:
            return order.total() * Decimal("0.07")
        return Decimal(0)


# --- Functional strategy ------------------------------------------------------

PromotionFunc = Callable[["Order"], Decimal]


@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: Sequence[LineItem]
    promotion: PromotionFunc | None = None

    def total(self) -> Decimal:
        return sum((item.total() for item in self.cart), start=Decimal(0))

    def due(self) -> Decimal:
        discount = Decimal(0) if self.promotion is None else self.promotion(self)
        return self.total() - discount


def fidelity_promo(order: Order) -> Decimal:
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal("0.05")
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal("0.10")
    return discount


def large_order_promo(order: Order) -> Decimal:
    distinct = {item.product for item in order.cart}
    if len(distinct) >= 10:
        return order.total() * Decimal("0.07")
    return Decimal(0)


promos_manual: list[PromotionFunc] = [fidelity_promo, bulk_item_promo, large_order_promo]


def best_promo_manual(order: Order) -> Decimal:
    return max(promo(order) for promo in promos_manual)


# --- Auto-registration via decorator -----------------------------------------

promos_registry: list[PromotionFunc] = []


def promotion(promo: PromotionFunc) -> PromotionFunc:
    promos_registry.append(promo)
    return promo


@promotion
def fidelity_promo2(order: Order) -> Decimal:
    return fidelity_promo(order)


@promotion
def bulk_item_promo2(order: Order) -> Decimal:
    return bulk_item_promo(order)


@promotion
def large_order_promo2(order: Order) -> Decimal:
    return large_order_promo(order)


def best_promo_registered(order: Order) -> Decimal:
    return max(promo(order) for promo in promos_registry)


def money(x: str) -> Decimal:
    return Decimal(x)


def main() -> None:
    joe = Customer("John Doe", 0)
    ann = Customer("Ann Smith", 1100)

    cart_bulk = [
        LineItem("banana", 30, money("0.50")),
        LineItem("apple", 10, money("1.50")),
    ]
    cart_large = [LineItem(f"item-{i}", 1, money("1.00")) for i in range(10)]

    print("=== classic (classes) ===")
    print("fidelity ->", OrderClassic(ann, cart_bulk, FidelityPromo()).due())
    print("bulk ->", OrderClassic(joe, cart_bulk, BulkItemPromo()).due())
    print("large ->", OrderClassic(joe, cart_large, LargeOrderPromo()).due())

    print("\n=== functional (functions) ===")
    print("fidelity ->", Order(ann, cart_bulk, fidelity_promo).due())
    print("bulk ->", Order(joe, cart_bulk, bulk_item_promo).due())
    print("large ->", Order(joe, cart_large, large_order_promo).due())

    print("\n=== best promo ===")
    o = Order(ann, cart_bulk, best_promo_manual)
    print("best_promo_manual -> discount:", o.promotion(o), "due:", o.due())
    o2 = Order(ann, cart_bulk, best_promo_registered)
    print("best_promo_registered -> discount:", o2.promotion(o2), "due:", o2.due())


if __name__ == "__main__":
    main()

