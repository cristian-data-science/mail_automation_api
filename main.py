from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
import secrets
import json

# Cargamos las variables de entorno y establecemos la clave de la API de OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Inicializamos la autenticación básica HTTP
security = HTTPBasic()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorizar y extraer información clave de un correo, como el caso de uso, nombre de la empresa que envía, detalles de contacto, la intención, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "Nombre de dominio de la persona que envía el correo. ej si la variable from_email es felipe@alto.com el companyName es alto"
                },
                "personName": {
                    "type": "string",
                    "description": "Nombre de la persona que envía el correo, Este se encuentra en el principio del correo. ej: De: Zdenka Skorin Milovic <zdenka.skorin@patagonia.com>"
                },
                "resumen": {
                    "type": "string",
                    "description": "resumir el mail en una oración pequeña, rescatando de la mejor manera posible el contexto general, no mas de 10 palabras"
                },                                                
                "priority": {
                    "type": "string",
                    "description": "Intenta dar una prioridad a este correo basándote en la importancia o urgencia que le da el remitente en categorías como las siguientes: 1. no urgente 2. medianamente urgente 3. muy urgente "
                },
                "category": {
                    "type": "string",
                    "description": "Intenta categorizar este correo en categorías como las siguientes: 1. Inventario 2. Importaciones; 3. Compra; 4. Equipo de operaciones; Reunion con USA, etc."
                },
                "tareas": {
                    "type": "string",
                    "description": "Intenta identificar las tareas que me piden realizar en el correo, separar las tareas en comas"
                },
                "nextStep":{
                    "type": "string",
                    "description": "Define el siguiente paso que recomiendas hacer para avanzar el tema especifico del correo."
                }
            },
            "required": ["companyName","resumen","personName", "amount", "salesOrder", "priority", "category", "nextStep"]
        }
    }
]



# Definimos el modelo de email
class Email(BaseModel):
    from_email: str
    content: str

# Función para validar las credenciales del usuario
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv('user_api'))
    correct_password = secrets.compare_digest(credentials.password, os.getenv('pass_api'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email, username: str = Depends(get_current_username)):
    try:
        content = email.content
        from_email = email.from_email
        query = f"Please extract key information from this email: {from_email + content} "
        messages = [{"role": "user", "content": query}]

        response = openai.ChatCompletion.create(
            #model="gpt-4-0613",
            model = "gpt-3.5-turbo-0613",
            messages=messages,
            functions = function_descriptions,
            function_call="auto"
        )

        arguments = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
        companyName = arguments.get("companyName")
        resumen = arguments.get("resumen")
        personName = arguments.get("personName")
        priority = arguments.get("priority")
        salesOrder = arguments.get("salesOrder")
        category = arguments.get("category")
        tareas = arguments.get("tareas")
        nextStep = arguments.get("nextStep")

        return {
            "companyName": companyName,
            "personName": personName,
            "resumen": resumen,
            "salesOrder": salesOrder,
            "priority": priority,
            "category": category,
            "tareas": tareas,
            "nextStep": nextStep
        }
    except Exception as e:
        return {"error": str(e)}