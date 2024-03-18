
import os
import json

os.environ["KEY_OPENIA"] = ""
os.environ["AWS_ACCESS_KEY_ID"] =""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_DEFAULT_REGION"] = ""


""" TEST S3 EXITOSO
from utils import download_s3
aws_storage_bucket_name = 'bots-tags-customer' 
embeddings_customer = "embeddings_customer1.json"
content = download_s3(file=embeddings_customer, aws_storage_bucket_name=aws_storage_bucket_name)
print(content)
"""


""" TEST ONBOARDING EXITOSO
from core_botsi.onboarding import OnboardingStateMachine
from customer_test.customer_01.mock_tag import TAG

openai_api_key = os.environ["KEY_OPENIA"]
model = "gpt-3.5-turbo-0613"
prompt_onboarding = "Tu mision actuar como un ASISTENTE que consulta en un SISTEMA y seguir la siguiente conversacion: 'USUARIO: Hola, ASISTENTE: Hola Bienvenido al sistema de registro, USUARIO: que dato necesitas?' y responder lo próximo que diria el ASISTENTE es español basado en la respuesta del SISTEMA: {system_onboarding}, y solicitando en español el dato: {question} que sirve para {description} y brindando un ejemplo de la siguiente expresion regular {format}, evita mostar la expresion regular dado que el usuario no entiende de expresiones regulares, los datos que ya tienes en tu memoria son: {data_provided} que te pueden servir para dar una atención mas personalizada. TEN EN CUENTA QUE NO ES NECESARIO SALUDAR OTRA VEZ" # , te voy a dar algunos ejemplos de como quiero que respondas: ejemplo 1: Podrias proporcionarme porfavor tu {question}?, ejemplo 2: Hasta el momento me has suministrado la siguiente información: {data_provided} ahora necesito tu {question}, ejemplo 3: Parece que no es correcto tu respuesta {question}, me indicas porfavor tu {question}

onboarding = OnboardingStateMachine(
    form_data=TAG["form_data"],
    consumer_info=TAG["consumer_info"],
    openai_api_key=openai_api_key,
    model=model,
    prompt_onboarding=prompt_onboarding
)

while True:
    msg = input("Humano: ")
    if msg == "exit":
        break
    response = onboarding.main_onboarding(user_input=msg)
    print("IA: ", response)
"""


from core_botsi.main_core import CoreChain
from langchain.schema import HumanMessage, AIMessage, ChatMessage
from customer_test.customer_01.mock_tag import TAG
from customer_test.customer_01.functions import langChaingFunctions

openai_api_key = os.environ["KEY_OPENIA"]
model = "gpt-3.5-turbo-16k"
aws_storage_bucket_name = 'bots-tags-customer'

core = CoreChain(
    tag=TAG, 
    openai_api_key=openai_api_key, 
    model=model,
    aws_storage_bucket_name=aws_storage_bucket_name
)

lang_chaing_functions = langChaingFunctions(
    tag=TAG, 
    products_customer=core.products_customer
)

def main_agent_chat(*, query_consumer):
    
    response = {}
    
    llm = core.llm
    
    core.onboarding.main_onboarding(user_input=query_consumer)
    
    core.onboarding.end_onboarding = True # test
    core.onboarding.collected_data = {'nombre': 'leo', 'producto': 'celulares', 'celular': '3004971594'}
    
    if core.onboarding.end_onboarding:
        core.data_param["data_provided"] = core.onboarding.collected_data
            
        for prompt in core.tag["prompts"]:
            core.messages.append(
                ChatMessage(
                    role=prompt["role"],
                    content=prompt["content"].format(**core.data_param["data_provided"])
                )
            )
        
        # Manejar el primer mensaje
        if core.ini:
            core.ini = False
            core.push_message(msg=
                HumanMessage(content="Hola")          
            )
        else:
            core.push_message(msg=
                HumanMessage(content=query_consumer)          
            )
        
        res_chat = llm.predict_messages(
            core.messages,
            functions=lang_chaing_functions.list_functions()
        )
                                    
        if res_chat.additional_kwargs:
            core.push_message(msg=
                AIMessage(content=str(res_chat.additional_kwargs))
            )

            for function in core.tag["functions_core"]:
                try:
                    import pdb
                    pdb.set_trace()
                    if json.loads(res_chat.additional_kwargs["function_call"]["arguments"]).get(function["parameters"][0]):
                        param = json.loads(res_chat.additional_kwargs["function_call"]["arguments"]).get(function["parameters"][0])
                        parameters = [param] * len(function["parameters"])
                        name_function = res_chat.additional_kwargs["function_call"]["name"]
                        
                        # Valida si existe el metodo y obtiene la función por nombre y ejecútala
                        if hasattr(lang_chaing_functions, function["name"]) and callable(getattr(lang_chaing_functions, function["name"])):
                            function_to_call = getattr(lang_chaing_functions, function["name"])
                            response = function_to_call(*parameters)
                            
                            core.push_message(msg=
                                ChatMessage(
                                    role="function",
                                    additional_kwargs={
                                        "name": name_function
                                    },
                                    content=str(response)
                                )
                            )
                                                        
                            res_chat_function = llm.predict_messages(
                                core.messages,
                                functions=lang_chaing_functions.list_functions()
                            )
                            
                            # Si pasa asesor                
                            if lang_chaing_functions.step_advisor:
                                return {
                                    "res_chat": res_chat_function.content,
                                    "rounting": core.data_param["data_provided"]["celular"],
                                    "data_capture": lang_chaing_functions.data_capture,
                                    "consumer_info": core.data_param,
                                    "end_chat": True,
                                    "step_advisor": True
                                }

                            response = {
                                "res_chat": res_chat_function.content,
                                "function": name_function,
                                "rounting": core.data_param["data_provided"]["celular"],
                                "end_chat": False,
                                "step_advisor": False
                            }
                except:
                    pass
            response["res_chat"] = res_chat_function.content # cuando pasa asesor
            response["rounting"] = core.data_param["data_provided"]["celular"]
            response["data_capture"] = lang_chaing_functions.data_capture

        else:
            response["res_chat"] = res_chat.content
            response["rounting"] = core.data_param["data_provided"]["celular"]   
            
        response["consumer_info"] = core.data_param
        response["end_chat"] = False
        response["step_advisor"] = False
        
        return response
    
    else:
        response["res_chat"] = core.onboarding.response_chat
        response["consumer_info"] = core.data_param
        response["end_chat"] = False
        response["step_advisor"] = False
        return response
        
while True:
    msg = input("Humano: ")
    if msg == "exit":
        break
    ia = main_agent_chat(query_consumer=msg)
    print("IA: ", ia)
    if ia["end_chat"] or ia["step_advisor"]:
        break
