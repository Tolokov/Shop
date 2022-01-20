import json
import random
import os


def generate_cards(pk, public_id, brand, category, price, name_product, path, condition, quantity):
    brand = str(brand)
    price = str(price)
    category = "".join(category)
    icon = f'fixtures/images/{path}'
    condition = "".join(condition)


    one_card = {
        "model": "Shop.Card_Product",
        "pk": pk,
        "fields": {
            "product_public_ID": public_id,
            "name": name_product,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "price": price,
            "availability": "False",
            "brand": brand,
            "category": category,
            "icon": icon,
            "condition": condition,
            "quantity": quantity
        }
    }
    return one_card


def get_pk(count=99999):
    for pk in range(2, count):
        yield pk


def main(how_many_cards):
    many_cards = list()
    pk = get_pk()
    paths = os.walk('C:\\Users\\Python DEV\\PycharmProjects\\DjangoWatchShop\\media\\fixtures\\images')
    names = paths.__next__()[2]


    while 1 < how_many_cards:
        public_id = random.randint(1000000, 9999999)
        brand = random.randint(1, 6)
        quantity = random.randint(1, 12)
        category = random.choices(['1', '2', '3', '4', '5', '6', '7'], k=2)
        price = round(random.uniform(333.33, 6666.66), 2)

        f_name = random.choices(['Джинсы', 'Брюки', 'Штаны'], k=1)
        l_name = random.choices(['', '', 'эстетичные', 'изящные', 'классические', 'с карманами', 'с пряжкой'], k=1)

        path = random.choices(names)[0]

        name_product = " ".join(f_name + l_name)
        condition = random.choices(['N', 'F', 'S'], k=1)

        one_card = generate_cards(pk.__next__(), public_id, brand, category, price, name_product, path, condition, quantity)
        many_cards.append(one_card)

        how_many_cards -= 1

    return many_cards


if __name__ == '__main__':
    result = main(99)
    print(result)
    with open('card_product.json', 'w') as j:
        j.write(json.dumps(result))
