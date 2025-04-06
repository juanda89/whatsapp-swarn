#agents_setup.py
import os
from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
load_dotenv()


# Configurar clave de API de OpenAI desde variables de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    set_default_openai_key(openai_api_key)

coordinador_estrategico = Agent(
    name="coordinador_estrategico",
    instructions="Eres el agente principal. Tu función es entender el contexto y la industria del creador de contenido. Pregunta a qué se dedica y recopila detalles útiles.",
)

creativo_ideas = Agent(
    name="creativo_ideas",
    instructions="Eres un generador creativo. Aportas ideas de contenido originales y novedosas adaptadas a la industria del usuario.",
)

guionista_visual = Agent(
    name="guionista_visual",
    instructions="Tomas una idea creativa y la desarrollas en un guion o storyboard para un video, reel, publicación o carrusel.",
)

programador_contenido = Agent(
    name="programador_contenido",
    instructions="Te encargas de preguntar la frecuencia con la que el usuario desea publicar, y luego armas una grilla de contenido semanal basada en esa frecuencia.",
)

alertador_publicacion = Agent(
    name="alertador_publicacion",
    instructions="Eres un agente que recuerda cuándo publicar. Das alertas según el horario previsto en la grilla.",
)

gestor_pagos = Agent(
    name="gestor_pagos",
    instructions="Tú sabes si un usuario ha pagado o no. Si no ha pagado, le envías un link de pago. Si ha pagado, le permites acceder al servicio normalmente.",
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Encárgate de pasar la solicitud al agente adecuado dependiendo del tipo de pregunta del usuario.",
    handoffs=[
        coordinador_estrategico,
        creativo_ideas,
        guionista_visual,
        programador_contenido,
        alertador_publicacion,
        gestor_pagos
    ],
)
# Diccionario de agentes disponibles para fácil acceso por nombre
AGENTS = {
    "coordinador_estrategico": coordinador_estrategico,
    "creativo_ideas": creativo_ideas,
    "guionista_visual": guionista_visual,
    "programador_contenido": programador_contenido,
    "alertador_publicacion": alertador_publicacion,
    "gestor_pagos": gestor_pagos,
    "assistant": triage_agent
}