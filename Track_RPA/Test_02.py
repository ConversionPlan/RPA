import requests
import pandas as pd

API = "c972c7e047d93bf6da9329c645154723:A:ZFhjOD8l1T6O2urWsiuLsvQ62PpuNHELMg21PRVwXbvQSOi2fgIzucOWeQ3rS6AUz1s02piupGVd7vMr0"
file = "C:\\Users\\Victor Angêlo\\OneDrive\\TRACK\\Development\\Python Development\\Automation\\Track_RPA\\Archives\\Test_Big.xlsx"
headers = {'Content-type': 'application/x-www-form-urlencoded',
                                            'Accept': 'application/json',
                                            'Authorization': API}

# Open the Table with Products
Tb = pd.read_excel(file)
for l, product in enumerate(Tb["product_name"]):
    item = Tb.loc[l, "item"]
    NDCOFICIAL = Tb.loc[l, "ndc"]
    LOT_NAME = Tb.loc[l, "lot_name"]

    GET_URL = 'https://api.test.tracktraceweb.com/2.0/products?identifier_us_ndc=' + NDCOFICIAL  # MAKE A GET WITH NDC

    # LINE THAT EXECUTES THE API WITH THE REQUESTS LIBRARY
    response = requests.get(GET_URL, headers=headers)

    if response.status_code == 200:  # IF RESPONSE IS POSITIVE
        response_dic = response.json()  # BRINGS A JSON DICTIONARY
        RA = response_dic['data'][0]  # PULLS THE UUID, WHICH IS THE FIRST TAG WITHIN THE DATA TAG
        uuid_products = (RA['uuid'])  # STORES IN A VARIABLE

        # HERE WE START THE PROCESS OF FINDING THE TRANSACTION UUID
        GET_URL = 'https://api.test.tracktraceweb.com/2.0/shipments?transaction_order_number=' + "PO_Teste_05792"  # MAKE A GET WITH THE SO NUMBER

        # LINE THAT EXECUTES THE API WITH THE REQUESTS LIBRARY
        response = requests.get(GET_URL, headers=headers)

        if response.status_code == 200:  # IF RESPONSE IS POSITIVE
            response_dic = response.json()  # BRINGS A JSON DICTIONARY
            RA = response_dic['data'][0]  # PULLS THE UUID, WHICH IS THE FIRST TAG WITHIN THE DATA TAG
            uuid_transactions = (RA['uuid'])  # STORES IN A VARIABLE

            # HERE WE START THE PROCESS OF SEARCHING FOR THE TRANSACTION SERIALS

            GET_URL = 'https://api.test.tracktraceweb.com/2.0/shipments/Inbound/' + uuid_transactions + '/serials?type=PRODUCT_LOT&serial_type=SIMPLE_SERIAL&product_uuid=' + uuid_products  # Do a GET with the PO and the UUID

            # LINE THAT EXECUTES THE API WITH THE REQUESTS LIBRARY
            response = requests.get(GET_URL, headers=headers)

            if response.status_code == 200:  # IF THE ANSWER IS POSITIVE

                response_dic = response.json()  # BRINGS A JSON DICTIONARY
                for number in response_dic:  # PRINT EACH ELEMENT WITHIN JSON

                    # HERE WE START THE PROCESS OF SEARCHING FOR THE GS1_SERIAL

                    GET_URL = 'https://api.test.tracktraceweb.com/2.0/serial_finder?serial_type=PRODUCT_SIMPLE_SERIAL&serials=' + number + '&product_uuid=' + uuid_products + '&lot_number=' + LOT_NAME + '&result_type=ON_SCREEN&_=1705526464100'  # Do a GET with the PO and the UUID

                    # LINE THAT EXECUTES THE API WITH THE REQUESTS LIBRARY
                    response = requests.get(GET_URL, headers=headers)

                    if response.status_code == 200:  # IF THE ANSWER IS POSITIVE
                        response_dic = response.json()  # BRINGS A JSON DICTIONARY
                        GS1_Serial_Value = response_dic['results'][0]['gs1_serial']  # PULLS THE GS1_SERIAL

                        print(GS1_Serial_Value)
                    else:
                        print(response.status_code)
