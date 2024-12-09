from behave import *
from datetime import datetime
from faker import Faker
from random import randint
from auth import *
import json

fake = Faker()

@given("User exists")
def starts_timer(context):
    context.initial_time = datetime.now().strftime("%H:%M:%S")

@given("Is Logged In")
def is_logged_in(context):
    launchBrowser(context)
    context.driver.implicitly_wait(5)
    openLoginURL(context, "https://demopharmacoltd.qa-test.tracktraceweb.com/auth")
    enterEmail(context, "rpa-user@tracktracerx.com")
    clickNextToLogin(context)
    enterPassword(context, "Rpa!1234")
    clickSubmitButton(context)

@then("End test")
def ends_timer(context):
    context.final_time = datetime.now().strftime("%H:%M:%S")
    with open("report/test_times.json", "r") as file:
        time_json = json.load(file)

    time_json.append({ "start": context.initial_time, "end": context.final_time })
    with open("report/test_times.json", "w") as file:
        file.write(json.dumps(time_json))

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
    gs1_id = generate_x_length_number(6)
    return gs1_id

def generate_gtin_with_cp_id(company_prefix: str, gs1_id: str) -> str:
    gtin = gs1_id[0] + company_prefix + gs1_id[1:]
    return gtin

def generate_ndc():
    ndc = f"{generate_x_length_number(3)}-{generate_x_length_number(4)}"
    return ndc

def generate_text_with_n_chars(n = 5) -> str:
    if n < 5 or n is None:
        n = 5
    text = fake.text(n)
    return text
