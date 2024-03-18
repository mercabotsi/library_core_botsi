TAG = {
    "intents": [],
    "prompts": [
        {
            "role": "system",
            "content": "Quiero que actúes como un asistente de ventas con el que estoy conversando. El prodcuto que debes vender res: {producto} puedes inventar un inventario de dicho producto para ofrecer. Nunca rompas el personaje. Expresa las ideas con pocas y adecuadas palabras y usa emojis para ser más amigable"
        },
        {
            "role": "system",
            "content": "Descripción: Dado el siguiente {producto} eres un experto en ventas, tu mision es vender usando las mejores tecnicas comerciales persuadiendo al cliente."
        },
        {
            "role": "system",
            "content": "El nombre del cliente es: {nombre}"
        },
        {
            "role": "assistant",
            "content": "Como puedo ayudarte con la informacion que tengo a cerca de {producto}?"
        }
    ],
    "prompt_onboarding": "Tu mision actuar como un ASISTENTE que consulta en un SISTEMA y seguir la siguiente conversacion: 'USUARIO: Hola, ASISTENTE: Hola Bienvenido al sistema de registro, USUARIO: que dato necesitas?' y responder lo próximo que diria el ASISTENTE es español basado en la respuesta del SISTEMA: {system_onboarding}, y solicitando en español el dato: {question} que sirve para {description} y brindando un ejemplo de la siguiente expresion regular {format}, evita mostar la expresion regular dado que el usuario no entiende de expresiones regulares, los datos que ya tienes en tu memoria son: {data_provided} que te pueden servir para dar una atención mas personalizada. TEN EN CUENTA QUE NO ES NECESARIO SALUDAR OTRA VEZ",
    "id_customer": 1,
    "type_chatbot": "ventas",
    "consumer_info": {},
    "form_data": [
        {
            "data": "nombre",
            "format": "^[A-Za-z\\s]+$",
            "description": "Nombre del usuario para una atención más personalizada"
        },
        {
            "data": "producto",
            "format": "^[A-Za-z\\s]+$",
            "description": "Un producto que el asistente de ventas venda como zapatos, celulares etc"
        },
        {
            "data": "celular",
            "format": "^\\d{10}$",
            "description": "Celular al cual se transferira a un asesor humano"
        }
    ],
    "shopping_cart": {},
    "functions_core": [
        {
            "name": "get_product_info",
            "parameters": [
                "detalle_producto"
            ]
        },
        {
            "name": "paso_asesor",
            "parameters": [
                "resumen_conversacion"
            ]
        },
        {
            "name": "capture_data_product",
            "parameters": [
                "resumen_conversacion"
            ]
        }
    ],
    "category_products": []
}