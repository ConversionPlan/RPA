# RPA

RPA for Track Trace RX's portal. It runs after every push to the `main` branch of this repository, and daily at 6am.

All tests in order:
1. Track Validation Report: It generates a PDF report of the test and saves it on our Min.IO bucket.
2. Checks for Admin: It checks for an admin in the Admin table.
3. Gets Serial by Transaction: It gets the products in a list, their transactions and serials.

# Run Locally

In order to run this repository locally, you need to have [Python](https://www.python.org/downloads/) installed.

After having clone this repository, to install all the necessary packages, go to the root directory and run:

`pip install -r requirements.txt`

Then, to run all the tests at the same time:

`bash run_tests.sh`

Or to run a specific test:

`python Track_RPA/tests/{SPECIFIC_TEST_PY}`

And replace {SPECIFIC_TEST_PY} by the name of the test file you want to run.

Note: The PDF file 001_Track_Validation_Report.py generates can be found in `Track_RPA/Archives/Detailed/Track_Validation.pdf`. 