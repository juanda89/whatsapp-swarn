# Importamos FastAPI para crear una API
from fastapi import FastAPI, Request
import openai
from dotenv import load_dotenv
import os

# Cargamos las variables del archivo .env
load_dotenv()

# Inicializamos la aplicación
app = FastAPI()

# Cargamos la API key de OpenAI desde la variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Definimos los agentes Swarm
agents = [
    {
        "name": "coordinador_estrategico",
        "instructions": (
            "Eres el agente principal. Tu función es entender el contexto y la industria "
            "del creador de contenido. Pregunta a qué se dedica y recopila detalles útiles."
        )
    },
    {
        "name": "creativo_ideas",
        "instructions": (
            "Eres un generador creativo. Aportas ideas de contenido originales y novedosas "
            "adaptadas a la industria del usuario."
        )
    },
    {
        "name": "guionista_visual",
        "instructions": (
            "Tomas una idea creativa y la desarrollas en un guion o storyboard para un video, "
            "reel, publicación o carrusel."
        )
    },
    {
        "name": "programador_contenido",
        "instructions": (
            "Te encargas de preguntar la frecuencia con la que el usuario desea publicar, y luego "
            "armas una grilla de contenido semanal basada en esa frecuencia."
        )
    },
    {
        "name": "alertador_publicacion",
        "instructions": (
            "Eres un agente que recuerda cuándo publicar. Das alertas según el horario previsto en la grilla."
        )
    },
    {
        "name": "gestor_pagos",
        "instructions": (
            "Tú sabes si un usuario ha pagado o no. Si no ha pagado, le envías un link de pago. "
            "Si ha pagado, le permites acceder al servicio normalmente."
        )
    }
]

# Creamos el endpoint al que n8n enviará el mensaje del usuario
@app.post("/webhook")
async def recibir_mensaje(request: Request):
    # Extraemos el JSON enviado desde n8n
    data = await request.json()
    mensaje_usuario = data.get("mensaje", "")

    # Creamos la conversación base
    mensajes = [
        {"role": "system", "content": "Eres un sistema de agentes expertos en contenido digital."},
        {"role": "user", "content": mensaje_usuario}
    ]

    # Llamamos a la API de OpenAI con los agentes Swarm
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=mensajes,
        agents=agents,
        tool_choice="auto"
    )

    # Obtenemos el texto de respuesta
    respuesta = response.choices[0].message.content

    # Devolvemos la respuesta en formato JSON
    return {"respuesta": respuesta}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
