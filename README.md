# RPA

RPA for Track Trace RX's portal. It runs after every push to the `main` branch of this repository, and daily at 6am.

All tests in order:
1. Login Feature.
   1. Login to Portal with valid parameters
2. Product Feature.
   1. Create an Each Product
   2. Create an Aggregation Product
   3. Delete a Product
3. Trading Partners Feature.
   1. Create a Vendor
   2. Create a Customer
4. Location Feature.
   1. Create a Customer's Location
5. Inbound.
   1. Create a Manual Inbound Shipment for an Each Product
   2. Create a Manual Inbound Shipment for a Case Product
   3. Manual Upload of EPCIS File - Currently testing manual file generation and upload, but not if the Inbound was created, as it is blocked in QA environment
   4. Delete Inbound
6. Outbound.
   1. Create a SO by Picking and Shipping at Once
   2. Delete Outbound
7. Inventory.
   1. Transfer Item
   2. Quaratine Item
   3. Destroy Item
   4. Report Missing/Stolen Item
   5. Dispense Item
   6. Transform Item
8. Manufacture.
   1. Manufacture Serials
   2. Delete Manufactured Serials
   3. Commission Serial Numbers
9. Container.
   1. Create a Container
   2. Delete a Container

# Run Locally

In order to run this repository locally, you need to have [Python](https://www.python.org/downloads/) installed.

After having cloned this repository, to install all the necessary packages, go to the root directory and run:

```
pip install -r requirements.txt
```

Then, to run all the tests at the same time:

```
behave
```

Or to run a specific test:

```
behave .\features\{SPECIFIC_FEATURE}
```

And replace {SPECIFIC_FEATURE} by the name of the feature file you want to run, such as `01-login.feature`.

If you want to run the tests headlessly, just run with `HEADLESS=True` before the command you want to use, for example:

```
HEADLESS=True behave
```

or

```
HEADLESS=True behave .\features\01-login.feature
```

## Report Generation

If you want to then generate the PDF report, you need to run the tests in a way that it generates a results JSON file using the following code:

```
behave --format json.pretty --outfile report\output\results.json
```

Then, to generate the PDF Report:

```
python .\reports\generate_pdf_py
```

The file will be found in `.\reports\Track_Validation.pdf`