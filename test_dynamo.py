from core_botsi import services

import os

os.environ["KEY_OPENIA"] = ""
os.environ["AWS_ACCESS_KEY_ID"] =""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_DEFAULT_REGION"] = ""


def test_insert_dynamobd():
    table_name = "customers_conversation"
    item = {
        'customer': "1",
        'conversation': 'valor1',
        'tag': 'valor2'
    }
    services.insert_dynamodb(table_name=table_name, item=item)


test_insert_dynamobd()
