from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypedDict, TypeVar

# ==========================
# TypedDict
# ==========================


class UserData(TypedDict):
    id: int
    name: str
    email: str


# ==========================
# Literal
# ==========================

Role = Literal["admin", "user", "guest"]


# ==========================
# Protocol
# ==========================


class Printable(Protocol):
    def display(self) -> str: ...


# ==========================
# Generic
# ==========================

T = TypeVar("T")


class Repository[T]:
    def __init__(self) -> None:
        self.items: list[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_all(self) -> list[T]:
        return self.items


# ==========================
# Dataclass
# ==========================


@dataclass
class User:
    id: int
    name: str
    email: str
    role: Role = "user"

    def display(self) -> str:
        return f"{self.name} ({self.role})"


# ==========================
# Functions
# ==========================


def print_object(obj: Printable) -> None:
    print(obj.display())


def create_user(data: UserData) -> User:
    return User(**data)


def get_email(user: User | None) -> str:
    if user is None:
        return "No email"

    return user.email


def square(value: int | float) -> int | float:
    return value * value


# ==========================
# Main
# ==========================


def main() -> None:
    repository = Repository[User]()

    data: UserData = {
        "id": 1,
        "name": "Juan",
        "email": "juan@email.com",
    }

    user = create_user(data)

    repository.add(user)

    print_object(user)

    print(get_email(user))

    print(square(12))

    print(square(5.5))

    print(repository.get_all())


if __name__ == "__main__":
    main()
