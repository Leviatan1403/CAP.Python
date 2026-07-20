from dataclasses import dataclass, field

from pydantic import BaseModel, Field, ValidationError, field_validator

# =====================================================================
# EJERCICIO 1: EL DOMINIO DE PRODUCTOS (Herencia, Composición y Dunder)
# =====================================================================


class Price:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency


class BaseProduct:
    def __init__(self, id: str, name: str, price: Price):
        self.id = id
        self.name = name
        self.price = price  # Composición: BaseProduct TIENE UN Price


class PhysicalProduct(BaseProduct):
    def __init__(self, id: str, name: str, price: Price, weight: float):
        super().__init__(id, name, price)
        self.weight = weight

    def __str__(self) -> str:
        return f"[Prod-{self.id}] {self.name} - {self.weight}kg - ${self.price.amount:.2f} {self.price.currency}"


# El dominio de ordenes(Dataclasses y Dunder de Comparación)


@dataclass
class Order:
    """Entidad de dominio que representa una Orden de Compra."""

    order_id: str
    customer_id: str
    items: list[PhysicalProduct]
    tax_rate: float = 0.16

    # Excluimos 'total' del constructor (__init__) ya que es un campo derivado
    total: float = field(init=False)

    def __post_init__(self):
        """Cálculo automático del total acumulado con impuestos."""
        subtotal = sum(item.price.amount for item in self.items)
        self.total = subtotal * (1 + self.tax_rate)

    def __eq__(self, other: object) -> bool:
        """Comparación de igualdad basada exclusivamente en el total."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.total == other.total

    def __lt__(self, other: "Order") -> bool:
        """Comparación 'menor que' basada exclusivamente en el total."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.total < other.total


# =====================================================================
# EJERCICIO 3: VALIDACIÓN Y SERIALIZACIÓN (Pydantic DTOs)
# =====================================================================


# --- Esquemas Internos de validación para Pydantic ---
class PriceSchema(BaseModel):
    amount: float = Field(gt=0, description="El monto debe ser mayor a cero")
    currency: str = Field(
        min_length=3, max_length=3, description="Código ISO de 3 letras"
    )


class ProductSchema(BaseModel):
    id: str
    name: str
    weight: float = Field(gt=0, description="El peso debe ser positivo")
    price: PriceSchema


# --- DTO de Entrada (Data Transfer Object) ---
class OrderIn(BaseModel):
    order_id: str
    customer_id: str
    items: list[ProductSchema]
    tax_rate: float = 0.16

    @field_validator("items")
    @classmethod
    def validate_items_not_empty(cls, v: list[ProductSchema]) -> list[ProductSchema]:
        """Asegura que la orden contenga al menos un producto."""
        if len(v) == 0:
            raise ValueError("La lista de productos no puede estar vacía.")
        return v

    def to_domain(self) -> Order:
        """Mapea el DTO validado hacia la Entidad de Dominio (Dataclass)."""
        domain_items = []
        for item in self.items:
            # Reconstruimos las instancias de dominio
            price_domain = Price(amount=item.price.amount, currency=item.price.currency)
            product_domain = PhysicalProduct(
                id=item.id, name=item.name, price=price_domain, weight=item.weight
            )
            domain_items.append(product_domain)

        return Order(
            order_id=self.order_id,
            customer_id=self.customer_id,
            items=domain_items,
            tax_rate=self.tax_rate,
        )


# --- DTO de Salida ---
class OrderOut(BaseModel):
    order_id: str
    customer_id: str
    total: float
    requires_shipping: bool

    @classmethod
    def from_domain(cls, order: Order) -> "OrderOut":
        """Mapea la Entidad de Dominio al DTO de salida."""
        # Lógica de negocio para salida: requiere envío si el peso total supera los 5kg
        total_weight = sum(item.weight for item in order.items)
        shipping_needed = total_weight > 5.0

        return cls(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total=round(order.total, 2),
            requires_shipping=shipping_needed,
        )


# =====================================================================
# SCRIPT DE VERIFICACIÓN / TEST DE INTEGRACIÓN
# =====================================================================


def ejecutar_pruebas() -> None:
    # print("=== INICIANDO PRUEBAS DEL LABORATORIO ===\n")

    # 1. Simulación de Payload JSON desde API externa
    payload_json = {
        "order_id": "ORD-2026-001",
        "customer_id": "CUST-404",
        "items": [
            {
                "id": "P01",
                "name": "Teclado Mecánico",
                "weight": 1.5,
                "price": {"amount": 120.0, "currency": "USD"},
            },
            {
                "id": "P02",
                "name": "Monitor Gamer 4K",
                "weight": 4.2,
                "price": {"amount": 450.0, "currency": "USD"},
            },
        ],
        "tax_rate": 0.16,
    }

    # 2. Validación de Entrada con Pydantic (OrderIn)
    print(" Paso 1: Validando JSON de entrada con Pydantic (OrderIn)")
    try:
        dto_entrada = OrderIn.model_validate(payload_json)
        print("JSON estructurado correctamente.")
    except ValidationError as e:
        print("Error de validación en JSON:", e.json())
        return

    # 3. Conversión de DTO a Entidad de Dominio (Dataclass)
    print("\n Paso 2: Convirtiendo DTO a Entidad de Dominio (Dataclass) ")
    orden_dominio_1 = dto_entrada.to_domain()
    print(f"Objeto generado: {type(orden_dominio_1).__name__}")
    print(
        f"Total calculado en la Dataclass (con IVA 16%): ${orden_dominio_1.total:.2f}"
    )
    print("Productos en la orden:")
    for item in orden_dominio_1.items:
        print(f"  - {item}")  # Invoca el __str__ de PhysicalProduct

    # 4. Prueba de Dunder Methods y Comparaciones
    print("\n Paso 3: Evaluando Lógica de Comparación")
    # Creamos una segunda orden directa más barata para comparar
    producto_barato = PhysicalProduct("P03", "Mouse Pad", Price(15.0, "USD"), 0.3)
    orden_dominio_2 = Order(
        order_id="ORD-2026-002", customer_id="CUST-404", items=[producto_barato]
    )

    print(f"Orden 1 Total: ${orden_dominio_1.total:.2f}")
    print(f"Orden 2 Total: ${orden_dominio_2.total:.2f}")
    # print(f"¿La Orden 2 es más barata que la Orden 1? (Orden 2 < Orden 1): {orden_dominio_2 < orden_dominio_1}")
    # print(f"¿La Orden 1 es igual en costo a la Orden 2? (Orden 1 == Orden 2): {orden_dominio_1 == orden_dominio_2}")

    # 5. Mapeo y generación de Respuesta de Salida (OrderOut)
    print("\n Paso 4: Generando DTO de Salida (OrderOut) ")
    dto_salida = OrderOut.from_domain(orden_dominio_1)
    print("JSON final enviado al cliente:")
    print(dto_salida.model_dump_json(indent=2))


if __name__ == "__main__":
    ejecutar_pruebas()
