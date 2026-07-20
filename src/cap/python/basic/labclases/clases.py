"""
LABORATORIO
Programación Orientada a Objetos + dataclasses + attrs + Pydantic

Conceptos incluidos:
- Clases
- Herencia
- Composición
- Dunder Methods
- dataclasses
- attrs
- Pydantic
- Conversión entre DTO y entidades
"""

from __future__ import annotations

from dataclasses import dataclass, field

from attrs import define, validators
from attrs import field as attr_field
from pydantic import BaseModel, ConfigDict, Field

# ======================================================
# attrs
# ======================================================


@define
class Product:
    """
    Clase utilizando attrs.

    Incluye validaciones automáticas.
    """

    id: int

    name: str = attr_field(
        validator=validators.and_(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )

    price: float = attr_field(
        validator=validators.and_(
            validators.gt(0),
        )
    )

    def __str__(self) -> str:
        return f"{self.name} (${self.price:.2f})"

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"


# ======================================================
# Herencia
# ======================================================


class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def display(self):
        return f"{self.name} <{self.email}>"


class Customer(Person):
    def __init__(self, customer_id: int, name: str, email: str):
        super().__init__(name, email)

        self.customer_id = customer_id

    def display(self) -> str:
        return f"Customer #{self.customer_id} {self.name}"


# ======================================================
# Composición
# ======================================================


@dataclass
class OrderItem:
    product: Product
    quantity: int

    @property
    def subtotal(self):
        return self.product.price * self.quantity


# ======================================================
# Dataclass principal
# ======================================================


@dataclass(order=True)
class Order:
    """
    Entidad del dominio.

    order=True permite comparaciones.
    """

    sort_index: float = field(init=False, repr=False)

    id: int

    customer: Customer

    items: list[OrderItem] = field(default_factory=list)

    discount: float = 0

    def __post_init__(self):
        if self.discount < 0:
            raise ValueError("Discount cannot be negative")

        self.sort_index = self.total

    # ------------------------------

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)

    @property
    def tax(self):
        return self.subtotal * 0.16

    @property
    def total(self):
        return self.subtotal + self.tax - self.discount

    # ------------------------------

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

        self.sort_index = self.total

    # ------------------------------

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"Order #{self.id} Total=${self.total:.2f}"

    def __repr__(self):
        return f"Order(id={self.id}, items={len(self.items)})"


# ======================================================
# Pydantic Entrada
# ======================================================


class OrderItemIn(BaseModel):
    product_id: int

    quantity: int = Field(gt=0)


class OrderIn(BaseModel):
    customer_id: int

    discount: float = Field(ge=0)

    items: list[OrderItemIn]


# ======================================================
# Pydantic Salida
# ======================================================


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    subtotal: float

    tax: float

    discount: float

    total: float


# ======================================================
# Base de datos simulada
# ======================================================

PRODUCTS = {
    1: Product(1, "Laptop", 1200),
    2: Product(2, "Mouse", 25),
    3: Product(3, "Keyboard", 50),
    4: Product(4, "Monitor", 350),
}

CUSTOMERS = {
    1: Customer(1, "Juan Perez", "juan@email.com"),
    2: Customer(2, "Maria Lopez", "maria@email.com"),
}


# ======================================================
# Conversión DTO -> Entidad
# ======================================================


def to_entity(order_in: OrderIn, order_id: int = 1) -> Order:
    customer = CUSTOMERS[order_in.customer_id]

    items = []

    for item in order_in.items:
        product = PRODUCTS[item.product_id]

        items.append(OrderItem(product, item.quantity))

    return Order(
        id=order_id, customer=customer, items=items, discount=order_in.discount
    )


# ======================================================
# Entidad -> DTO
# ======================================================


def to_output(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        subtotal=order.subtotal,
        tax=order.tax,
        discount=order.discount,
        total=order.total,
    )


# ======================================================
# Main
# ======================================================


def main() -> None:
    incoming_json = {
        "customer_id": 1,
        "discount": 100,
        "items": [
            {
                "product_id": 1,
                "quantity": 1,
            },
            {
                "product_id": 2,
                "quantity": 2,
            },
            {
                "product_id": 4,
                "quantity": 1,
            },
        ],
    }

    print("=" * 60)
    print("VALIDACIÓN CON PYDANTIC")
    print("=" * 60)

    order_in = OrderIn.model_validate(incoming_json)

    print(order_in)

    print()

    print("=" * 60)
    print("CONVERSIÓN A ENTIDAD")
    print("=" * 60)

    order = to_entity(order_in)

    print(order)

    print()

    print("Cliente:")

    print(order.customer.display())

    print()

    print("=" * 60)
    print("PRODUCTOS")
    print("=" * 60)

    for item in order.items:
        print(item.product, "| Cantidad:", item.quantity, "| Subtotal:", item.subtotal)

    print()

    print("=" * 60)
    print("CÁLCULOS")
    print("=" * 60)

    print("Subtotal :", order.subtotal)
    print("IVA      :", order.tax)
    print("Descuento:", order.discount)
    print("TOTAL    :", order.total)

    print()

    print("=" * 60)
    print("DUNDER METHODS")
    print("=" * 60)

    print("Cantidad de items:", len(order))

    another = Order(id=2, customer=order.customer, items=order.items)

    print("order < another :", order < another)

    print()

    print("=" * 60)
    print("SERIALIZACIÓN")
    print("=" * 60)

    output = to_output(order)

    print(output.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
