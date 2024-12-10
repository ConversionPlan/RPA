# RPA

RPA for Track Trace RX's portal. It runs after every push to the `main` branch of this repository, and daily at 6am.

All tests in order:
1. Login Feature.
   1. Login to Portal with valid parameters
2. Product Feature.
   1. Create an Each Product
   2. Create an Aggregation Product
3. Trading Partners Feature.
   1. Create a Vendor
   2. Create a Customer
3. Location Feature.
   1. Create a Customer's Location
4. Inbound.
   1. Create a Manual Inbound Shipment

# Run Locally

In order to run this repository locally, you need to have [Python](https://www.python.org/downloads/) installed.

After having clone this repository, to install all the necessary packages, go to the root directory and run:

```pip install -r requirements.txt```

Then, to run all the tests at the same time:

```behave --format json.pretty --outfile report/results.json```

Or to run a specific test:

```behave .\features\{SPECEFICI_TEST_PY}.feature --format json --outfile report/results.json```

And replace {SPECIFIC_TEST_PY} by the name of the test you want to run.

Then, to generate the PDF Report:

```python .\reports\generate_pdf_py```

The file will be found in `.\reports\Track_Validation.pdf`