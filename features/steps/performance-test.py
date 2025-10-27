from behave import when
from features.steps.auth import ends_timer
import os
import datetime


@when("Perform Test on {page} {url}")
def perform_test(context, page, url):
    try:
        now = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        command = f"lighthouse {url} --port=9222 --output=html --output-path=report/output/lighthouse_{page.lower()}_{now}.html"
        os.system(command)
    except Exception as e:
        ends_timer(context, e)
        raise
