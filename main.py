from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# Definimos los agentes
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

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    mensaje_usuario = data.get("mensaje", "")

    # ⚠️ Creamos el cliente DENTRO del endpoint, no al inicio del script
    print("CLAVE DE API:", os.getenv("OPENAI_API_KEY"))

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    mensajes = [
        {"role": "system", "content": "Eres un sistema de agentes expertos en contenido digital."},
        {"role": "user", "content": mensaje_usuario}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=mensajes,
        agents=agents,
        tool_choice="auto"
    )

    return {"respuesta": response.choices[0].message.content}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
