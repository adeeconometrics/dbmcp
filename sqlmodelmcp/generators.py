from typing import List
from random import uniform, randint, choice
from faker import Faker
from models import User, Product, Order, OrderItem, OrderStatus, Address, Category
from dataenums import Categiories, LaptopModels, SmartphoneModels, HeadphoneModels, MonitorModels, KeyboardModels, MouseModels, PrinterModels, TabletModels, SmartwatchModels, CameraModels

fake = Faker('en_PH')


def generate_addresses(n: int) -> List[str]:
    """Generate a list of fake address IDs."""
    return [
        Address(
            street=fake.street_address(),
            city=fake.city(),
            # state=fake.state(),
            zip_code=fake.postcode(),
            country=fake.country()
        ) for _ in range(n)
    ]


def generate_users(n: int, address_ids: List[str]) -> List[User]:
    """Generate a list of User instances. Requires a list of address_ids to bind addresses."""
    # For demo, generate addresses and assign randomly
    users = []
    for _ in range(n):
        firstname = fake.first_name()
        lastname = fake.last_name()
        users.append(
            User(
                firstname=firstname,
                lastname=lastname,
                email=f"{firstname.lower()}{lastname.lower()}@example.com",
                password=fake.password(),
                payment_info=fake.credit_card_number(),
                address_id=choice(address_ids)
            )
        )
    return users


def generate_categories() -> List[Category]:
    """Generate a list of Category instances."""
    return [
        Category(name=cat.value, description=cat.value)
        for cat in Categiories
    ]


def generate_products(n: int, category_id_map: dict) -> List[Product]:
    """Generate a list of Product instances with coherent category name and id."""
    CATEGORY_MODEL_MAP = {
        Categiories.LAPTOP: LaptopModels,
        Categiories.SMARTPHONE: SmartphoneModels,
        Categiories.HEADPHONES: HeadphoneModels,
        Categiories.MONITOR: MonitorModels,
        Categiories.KEYBOARD: KeyboardModels,
        Categiories.MOUSE: MouseModels,
        Categiories.PRINTER: PrinterModels,
        Categiories.TABLET: TabletModels,
        Categiories.SMARTWATCH: SmartwatchModels,
        Categiories.CAMERA: CameraModels,
    }
    products = []
    for _ in range(n):
        category = choice(list(Categiories))
        model_enum = CATEGORY_MODEL_MAP[category]
        model = choice(list(model_enum))
        category_name = category.value
        category_id = category_id_map[category_name]
        products.append(
            Product(
                name=model.value,
                price=round(uniform(10.0, 2500.0), 2),
                stock_quantity=randint(10, 1_000),
                category_id=category_id,
                category_name=category_name
            )
        )
    return products


def generate_orders(n: int, user_ids: List[int]) -> List[Order]:
    """Generate a list of Order instances."""
    return [
        Order(
            user_id=fake.random_element(elements=user_ids),
            order_date=fake.date_time_this_year(),
            status=(fake.random_element(elements=list(OrderStatus))).value
        ) for _ in range(n)
    ]


def generate_order_items(n: int, order_ids: List[str], product_ids: List[str]) -> List[OrderItem]:
    """Generate a list of OrderItem instances with unique (order_id, product_id) pairs."""
    pairs: set[tuple[str, str]] = set()
    items: list[OrderItem] = []
    max_possible = len(order_ids) * len(product_ids)
    n = min(n, max_possible)  # Prevent infinite loop if n > possible pairs

    while len(items) < n:
        order_id = choice(order_ids)
        product_id = choice(product_ids)
        if (order_id, product_id) not in pairs:
            pairs.add((order_id, product_id))
            items.append(OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=randint(1, 10)
            ))
    return items
