from faker import Faker
from random import randint
fake = Faker()

def generate_product_name() -> str:
    word_list = fake.get_words_list()
    product_name = "RPA"
    for i in range(4):
        product_name += f" {word_list[randint(0, len(word_list))].capitalize()}"

    return product_name


def generate_x_length_number(x: int) -> str:
    number = ""
    for i in range(x):
        number += str(randint(0, 9))

    return number


def generate_company_prefix() -> str:
    company_prefix = "0" + generate_x_length_number(6)
    return company_prefix


def generate_gs1_id() -> str:
    gs1_id = "0" + generate_x_length_number(5)
    return gs1_id


def generate_gtin_with_cp_id(company_prefix: str, gs1_id: str) -> str:
    gtin = gs1_id[0] + company_prefix + gs1_id[1:]
    return gtin


def generate_ndc():
    ndc = f"{generate_x_length_number(3)}-{generate_x_length_number(4)}"
    return ndc


def generate_text_with_n_chars(n=5) -> str:
    if n < 5 or n is None:
        n = 5
    text = fake.text(n)
    return text


def generate_cp_id_by_gtin(gtin: str) -> [str, str]:
    id = gtin[0] + gtin[8:]
    cp = gtin[1:8]
    return [cp, id]
