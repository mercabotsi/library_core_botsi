# Librarys
import json

# internal
# from core_botsi import services 

class langChaingFunctions:
    def __init__(self, tag: dict, products_customer: dict) -> None:
        self.tag = tag
        self.products_customer = products_customer
        self.end_chat = False
        self.step_advisor = False
        self.data_capture = []

    # functions LangChain
    
    def get_product_info(self, detalle_producto: str):
        self.data_capture.append(detalle_producto)
        product_inventory = f"Proponer productos inventados de {detalle_producto} e indagar que producto especifico necesita"
        response = {
            "name": product_inventory
        }
        return json.dumps(response)
    
    def capture_data_product(self, detalle_producto: str):
        self.data_capture.append(detalle_producto)
        product_inventory = f"Capturar dellates de productos como, color, tamaño, precio, marca etc {detalle_producto}"
        response = {
            "name": product_inventory
        }
        return json.dumps(response)
        
    def paso_asesor(self, resumen_conversacion: str):
        self.end_chat = True
        self.step_advisor = True
        msg = f"Pasar Asesor Humano"
        response = {
            "response": msg
        }
        return json.dumps(response)


    def list_functions(self) -> list:
        return [
            {
                "name": "get_product_info",
                "description": "Si lo que solicita el usuario parece ser un producto entonces suministrar mas informacion de dicho producto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "detalle_producto": {
                            "type": "string",
                            "description": "Informar detalles del producto, como color, tamaño, nombre, precio etc.",
                        }
                    },
                    "required": ["detalle_producto"],
                },
            },
            {
                "name": "capture_data_product",
                "description": "Si el usuario suministra informacion de su producto en question entonces capturarla.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "detalle_producto": {
                            "type": "string",
                            "description": "Capturar el detalle del producto.",
                        }
                    },
                    "required": ["detalle_producto"],
                },
            },
            {
                "name": "paso_asesor",
                "description": "Si lo que solicita es hablar con un asesor humano ó agente profesional humano.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resumen_conversacion": {
                            "type": "string",
                            "description": "Pasar Asesor",
                        }
                    },
                    "required": ["resumen_conversacion"],
                },
            }
        ]
