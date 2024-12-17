from faker import Faker
from random import randint

fake = Faker()


def generate_product_name() -> str:
    word_list = fake.get_words_list()
    product_name = "[RPA]"
    for i in range(4):
        product_name += f" {word_list[randint(0, len(word_list))].capitalize()}"

    return product_name


def generate_trading_partner_name() -> str:
    trading_partner_name = "[RPA] " + fake.company()
    return trading_partner_name


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


def generate_ndc() -> str:
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


def calculate_check_digit(base: str) -> int:
    weights = [3 if i % 2 == 0 else 1 for i in range(len(base))]
    total = sum(int(digit) * weight for digit, weight in zip(reversed(base), weights))
    remainder = total % 10
    return (10 - remainder) if remainder != 0 else 0


def generate_gln(company_prefix: str) -> str:
    gln = company_prefix + generate_x_length_number(5)
    check_digit = calculate_check_digit(gln)
    gln += str(check_digit)
    return gln


def generate_sgln_from_gln(gln: str) -> str:
    company_prefix = gln[:7]
    location_reference = gln[7:12]
    sgln_base = f"{company_prefix}.{location_reference}.0"
    sgln = f"urn:epc:id:sgln:{sgln_base}"
    return sgln


def generate_address() -> str:
    address = fake.address()
    return address


def generate_city() -> str:
    city = fake.city()
    return city


def generate_zip() -> str:
    zip = fake.zipcode()
    return zip


def generate_po() -> str:
    po = "PO#" + generate_x_length_number(9)
    return po


def generate_ref_number() -> str:
    ref = "REF#" + generate_x_length_number(9)
    return ref
