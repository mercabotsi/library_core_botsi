# Standard Library
import re

# External Library
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


class OnboardingStateMachine:
    def __init__(
        self,
        *,
        form_data: dict,
        consumer_info: dict,
        openai_api_key: str,
        model: str,
        prompt_onboarding: str
    ):
        self.prompt_onboarding = prompt_onboarding
        self.llm = ChatOpenAI(
            model=model, 
            openai_api_key=openai_api_key, 
            temperature=0
        )
        self.ini = True
        self.form_data = self.format_format(
            form_customer=form_data
        )
        self.current_step = 0
        self.collected_data = {}
        self.end_onboarding = False
        self.response_chat = ""
        self.consumer_info = consumer_info

    def validate_input(
        self,
        *,
        user_input: str
    ) -> str:
        data = self.form_data[self.current_step]
        data_name = data["data"]
        data_format = data["format"]

        if re.match(data_format, user_input):
            self.collected_data[data_name] = user_input
            self.current_step += 1
            if self.current_step < len(self.form_data):
                return f"Por favor, ingrese su {self.form_data[self.current_step]['data']}:"
            else:
                return "¡Onboarding completado!"
        else:
            return f"El formato de {data_name} es incorrecto. Por favor, inténtelo de nuevo."

    def format_format(
        self,
        *,
        form_customer:list
    ) -> list:
        for item in form_customer:
            if 'format' in item:
                formato = item['format']
                if not formato.startswith(r'^'):
                    item['format'] = r'^' + formato
                if not formato.endswith('$'):
                    item['format'] += r'$'
        return form_customer

    def chat_onboarding(
        self, 
        *, 
        question: str, 
        format: str, 
        description: str,
        data_provided: str, 
        system_onboarding: str
    ) -> str:
        prompt_template = PromptTemplate.from_template(self.prompt_onboarding)
        prompt = prompt_template.format(
            question=question,
            format=format,
            description=description,
            data_provided=data_provided,
            system_onboarding=system_onboarding
        )
        response = self.llm.predict(prompt)
        return response
    
    def find_missing_key(
        self,
        *,
        key_list: list,
        data_dict: dict
    )-> str:
        for key in key_list:
            if key not in data_dict:
                return key
        return None

    def main_onboarding(self, *, user_input:str):
        # validate_format() pendiente implementar validado format form_data
        """
        Los campos del form_data cuando se pasan a chat_onboarding deberia ser 
        dinamico con el fin de que se puedan añadir nuevos valores a form_data 
        y mapearlos desde el prompt sin afectar la funcionalidad del core onboarding
        """
        if not self.consumer_info:            
            data_to_request = [data["data"] for data in self.form_data]
            
            self.response_chat = self.chat_onboarding(
                question=data_to_request[0],
                format=self.form_data[0]["format"],
                description=self.form_data[0]["description"],
                data_provided="Ninguna",
                system_onboarding="Por favor ingrese: " + data_to_request[0]
            )
            
            # Manejar el primer mensaje
            if self.ini:
                self.ini = False
                return self.response_chat
            
            if self.current_step < len(self.form_data):
                system_onboarding = self.validate_input(
                    user_input=user_input
                )            

                question = self.find_missing_key(
                    key_list=data_to_request,
                    data_dict=self.collected_data
                )

                format = [
                    format["format"] for format in self.form_data if format["data"] == question
                ]
                
                description = [
                    description["description"] for description in self.form_data if description["data"] == question
                ]
                
                if isinstance(question, str):
                    self.response_chat = self.chat_onboarding(
                        question=question,
                        format=format,
                        description=description,
                        data_provided=self.collected_data,
                        system_onboarding=system_onboarding
                    )
                    return self.response_chat
                else:
                    self.end_onboarding = True
                    return self.collected_data
            else:
                self.end_onboarding = True
                return self.collected_data
        
        else:
            self.end_onboarding = True
            self.collected_data = self.consumer_info
            return self.collected_data
