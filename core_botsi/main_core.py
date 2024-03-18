# Standard Library
import os
import json

# External Library
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage

# Internal Library
from core_botsi.onboarding import OnboardingStateMachine
from settings.utils import save_content_s3, download_s3
from settings.settings import logger
from core_botsi import services


log = logger



MAX_MESSAGES = 22

class CoreChain:
    def __init__(
        self, 
        *, 
        tag: dict, 
        openai_api_key: str,
        model: str,
        aws_storage_bucket_name: str
    ) -> None:
        self.ini = True
        self.tag = tag
        self.id_customer = tag["id_customer"]
        self.messages = []
        self.data_param = {"data_provided":""}
        self.llm = ChatOpenAI(
            model=model, 
            openai_api_key=openai_api_key, 
            temperature=0
        )
        self.onboarding = OnboardingStateMachine(
            form_data=tag["form_data"],
            consumer_info=tag["consumer_info"],
            openai_api_key=openai_api_key,
            model=model,
            prompt_onboarding=tag["prompt_onboarding"]
        )
        self.aws_storage_bucket_name = aws_storage_bucket_name
        self.products_customer = self.generate_embeddings_customer()      

    def generate_embeddings_customer(self):
        embeddings_customer = "embeddings_customer" + str(self.id_customer) + ".json"
        content = download_s3(
            file=embeddings_customer, 
            aws_storage_bucket_name=self.aws_storage_bucket_name
        )
        if content is not None:
            products_customer = content
        else:
            products_customer = services.system_embedding_v2(
                tag=self.tag
            )
            save_content_s3(
                content=products_customer,
                name_file=embeddings_customer,
                aws_storage_bucket_name=self.aws_storage_bucket_name
            )
        return products_customer
    
    def generate_embeddings_customer_local(self):
        embeddings_customer = "embeddings_customer" + str(self.id_customer) + ".json"
        if os.path.exists(embeddings_customer):
            with open(embeddings_customer, "r") as archivo:
                products_customer = json.load(archivo)
        else:
            products_customer = services.system_embedding_v2(
                tag=self.tag
            )
            with open(embeddings_customer, "w", encoding="utf-8") as archivo:
                json.dump(products_customer, archivo, ensure_ascii=False)
        return products_customer

    def push_message(self, *, msg: str):
        self.messages.append(msg)
        functions = [
            message.role for message in self.messages if isinstance(message, ChatMessage)
        ].count("function")
        ai_human_messages = len([
            message for message in self.messages
                if isinstance(message, HumanMessage) or isinstance(message, AIMessage)
        ])
        
        if functions + ai_human_messages > MAX_MESSAGES:
            mensajes_excedentes = len(self.messages) - MAX_MESSAGES
            if (
                self.messages[:mensajes_excedentes][0].role in ("function") 
                or isinstance(self.messages[:mensajes_excedentes][0], HumanMessage) 
                or isinstance(self.messages[:mensajes_excedentes][0], AIMessage)
            ):
                del self.messages[:mensajes_excedentes]  # Elimina los datos más antiguos

