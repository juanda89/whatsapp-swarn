# main.py
import os
from fastapi import FastAPI, Request
from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI()

# Agentes definidos
spanish_agent = Agent(
    name="Spanish agent",
    instructions="Responde solamente en español, como experto en redes sociales para negocios.",
)

english_agent = Agent(
    name="English agent",
    instructions="Respond only in English, as a content strategy expert.",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Responde el mensaje o transfiérelo al agente correcto según el idioma.",
    handoffs=[spanish_agent, english_agent],
)

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    mensaje_usuario = data.get("mensaje", "")

    print("🔥 WEBHOOK RECIBIDO:", mensaje_usuario)

    try:
        result = await Runner.run(triage_agent, input=mensaje_usuario)
        return {"respuesta": result.final_output}
    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)