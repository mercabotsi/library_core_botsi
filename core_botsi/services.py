
import uuid

from settings.settings import logger

import openai 
from openai.embeddings_utils import get_embedding, cosine_similarity

import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError


logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

model_embedding = "text-embedding-3-small"

def validate_json_structure(
    *,
    tag: dict
) -> bool:
    estructura_esperada = {
        "id_customer": int,
        "consumer_info": dict,
        "type_chatbot": str,
        "category_products": list,
        "intents": list,
        "form_customer": list,
        "functions_core": list,
        "shopping_cart": dict,
        "prompts": list
    }
    for clave, tipo_esperado in estructura_esperada.items():
        if clave not in tag:
            return False
        if not isinstance(tag[clave], tipo_esperado):
            return False
    
    return True


def seek_response_to_intention(
        *,
        openai_api_key: str, 
        seek:str,
        tag: dict,
        products_customer: dict
    ) -> dict:
        """
        buscar el producto en el inventario de productos por medio de embeddings 
        Este metodo tiene dos tipos de busquedas
        1. Por producto y retornar el producto con la estructura correcta
        2. Por categoria de productos y retorna el listado de productos de esa categoria
        """
        openai.api_key = openai_api_key
        n_word_embed = get_embedding(
            seek,
            engine=model_embedding
        )
        aux_sim = 0
        aux_text_sought = ""
        for embeddings in products_customer["embeddings"]:
            word_compare = embeddings
            similitud = cosine_similarity(
                products_customer["embeddings"][word_compare],
                n_word_embed
            )
            if similitud > aux_sim:
                aux_sim = similitud
                aux_text_sought = word_compare
        if aux_sim > 0.81:
            # si la respuesta es una categoria, retornar los productos de dicha categoria
            for item in tag["category_products"]:
                if item["category"] == aux_text_sought:
                    aux_text_sought=item["products"]
                    break
            return {
                "product": aux_text_sought
            } 
        else:
            return None


def system_embedding_v2(*, tag: dict) -> dict:
        embeddings = {}
        try:
            for category in tag["category_products"]:
                embeddings[category["category"]] = get_embedding(
                    category["category"], 
                    engine=model_embedding
                )
                for product in category["products"]:
                    embeddings[product] = get_embedding(
                    product,
                    engine=model_embedding
                )
            for intent in tag["intents"]:
                embeddings[intent["intent"]] = get_embedding(
                    intent["intent"], 
                    engine=model_embedding
                )
            tag["embeddings"] = embeddings
        except Exception as e:
            print(f"Error :: {str(e)}")

        return tag

# DYNAMO
def insert_dynamodb(
    *,
    table_name: str,
    item: str
):
    dynamodb = boto3.resource('dynamodb')
    tabla = dynamodb.Table(table_name)
    try:
        respuesta = tabla.put_item(Item=item)
        logging.info(f"Item insertado exitosamente: {respuesta}")
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    except BotoCoreError as e:
        logging.error(e)
