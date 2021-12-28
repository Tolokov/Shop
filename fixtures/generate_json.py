import json
import random


def generate_cards(pk, public_id, brand, category, price):
    brand = str(brand)
    price = str(price)
    category = "".join(category)

    one_card = {
        "model": "Shop.Card_Product",
        "pk": pk,
        "fields": {
            "product_public_ID": public_id,
            "name": "product1",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "price": price,
            "availability": "False",
            "brand": brand,
            "category": category,
            "icon": "fixtures/card/s1.jpg"
        }
    }
    return one_card


def get_pk(count=99999):
    for pk in range(2, count):
        yield pk


def main(how_many_cards):
    many_cards = [
        {
            "model": "Shop.Card_Product",
            "pk": 1,
            "fields": {
                "product_public_ID": 1000000,
                "name": "product1",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                "price": "21.12",
                "availability": "True",
                "brand": "1",
                "category": "1",
                "icon": "fixtures/card/s1.jpg"
            }
        }
    ]
    pk = get_pk()


    while 1 < how_many_cards:
        public_id = random.randint(1000000, 9999999)
        brand = random.randint(1, 5)
        category = random.choices(['1', '2', '3', '4', '5', '6'], k=2)
        price = round(random.uniform(33333.33, 66666.66), 2)

        one_card = generate_cards(pk.__next__(), public_id, brand, category, price)
        many_cards.append(one_card)

        how_many_cards -= 1

    return many_cards


if __name__ == '__main__':
    result = main(99)
    print(result)
    with open('card_product.json', 'w') as j:
        j.write(json.dumps(result))
