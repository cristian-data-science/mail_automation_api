import requests
import json

url = 'http://localhost:10000'  # Cambia esto a la URL de tu API si no es esta
data = {
    "from_email": "zeta@patagonia.com",
    "content": """
    
Hola hola,

Les escribo porque CCSS y eCommerce tomaron la propuesta de @Cesar Orostegui de crear las reparaciones de traje de agua a través de ALOHA como "productos comprables" desde Shopify y me entró la duda respecto a como lo vamos a manejar desde el ERP y OMS

Les dejo mis dudas y les cito una reunión para que veamos como las resolvemos:
1.	Como se reflejaría un producto tipo servicio en el ERP? se le tienen que cargar unidades?
2.	Estos serían enviado en el masivo que recibe OMS para cargar inventario en shopify?
3.	Nos conviene crearlos como servicios o como productos?
4.	En el caso de que entre una orden con el servicio y además agregue un producto, qué bodega se le asignaría a ese servicio? si fuese CD nos toparíamos con productos que el CD no tiene que pickear. @Juan Simunovic esto generaría conflicto?
Les agendo una reunión corta para conversarlo, pero ideal si le dan una vuelta antes a los puntos

Saludos







"""
}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)  # Debería imprimir 200 si todo salió bien
print(response.json())  # Imprime la respuesta de la API
