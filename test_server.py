import requests
import json

print(
    requests.post(
        "http://127.0.0.1:10000",
        json={
            "from_email": "zeta@patagonia.com",
            "content": """
                Hola team! 

                Les quería comentar que hoy me puse en contacto con Jon, el Head de Tecnología Global de Patagonia, para darle visibilidad a nuestra situación con Axxon y explorar posibles soluciones que quizás no hayamos considerado hasta ahora.

                Lo más probable es que posterior al mail que le envié surja una reunión de teams, por lo que me gustaría que vayamos pensando en algunas preguntase nos interesaría plantear a Jon, entendiendo que el foco principal es el manejo del soporte y proyectos asociados a D365. Por mi lado creo interesante conocer:

                1.	Como trabaja actualmente USA, si tienen todo externalizado o si hay parte que trabajen internamente
                2.	Me gustaría entender la magnitud de proyectos y mejoras que están abordando continuamente
                3.	Cuál es su nivel de independencia para generar cierto tipo de servicios desde y hacia el ERP
                4.	Revisar los tiempos de trabajo promedio que manejan con su proveedor para pasos de versión, conexiones estándar (mínimo 100 HH por nuestro lado)
                Así que feliz de que generemos un pack de puntos a revisar con Jon

                Quedo atenta

                Saludos
            """
        }
    ).json()
)


