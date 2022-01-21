import json


def get_card(key, product):
    card = {
        "model": "Shop.ProductImage",
        "pk": key,
        "fields": {
            "title": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ",
            "product": product,
            "image": "fixtures/card/s1.jpg"
        }
    }
    return card


def generate_cards():
    many_cards = list()

    p_key = 2
    for i in range(1, 8):
        for product in range(1, 98):
            many_cards.append(get_card(key=p_key, product=product))
            p_key += 1

    return many_cards


def main():
    many_cards = generate_cards()
    return many_cards


if __name__ == '__main__':
    pass
    # result = main()
    # with open('../images_for_card.json', 'w') as j:
    #     j.write(json.dumps(result))
