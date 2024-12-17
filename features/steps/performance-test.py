from behave import when
from features.steps.auth import ends_timer
import os
import datetime


@when("Perform Test on {url}")
def perform_test(context, url):
    try:
        now = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        command = f"lighthouse {url} --port=9222 --output=html --output-path=report/lighthouse_{now}.html"
        os.system(command)
    except:
        ends_timer(context)
        raise
