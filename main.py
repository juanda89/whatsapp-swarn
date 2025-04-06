#main.py
import os
import asyncio
from flask import Flask, request, jsonify
from agents_setup import AGENTS  # Importar diccionario de agentes base
from models import SessionLocal, ConversationMemory
from agents import Runner

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Obtener datos del mensaje entrante (ajustar claves según formato de entrada)
    data = request.get_json(force=True)
    user_id = data.get("user_id") or data.get("From")  # ID único del usuario (ej: número WhatsApp)
    message_text = data.get("message") or data.get("Body")  # Texto del mensaje del usuario
    agent_name = data.get("agent", "assistant")  # Agente objetivo (por defecto "assistant")
    if agent_name not in AGENTS:
        agent_name = "assistant"  # Usa agente por defecto si no es válido

    # Iniciar sesión de DB y recuperar memoria conversacional previa
    db = SessionLocal()
    memory_entry = db.query(ConversationMemory).filter_by(user_id=user_id, agent_name=agent_name).first()
    if memory_entry and memory_entry.messages:
        conversation = list(memory_entry.messages)  # copiar lista existente
    else:
        conversation = []  # iniciar nueva conversación si no existe

    # Añadir el mensaje actual del usuario a la conversación
    conversation.append({"role": "user", "content": message_text})

    # Clonar el agente base para este usuario (preserva instrucciones del agente)
    base_agent = AGENTS[agent_name]
    agent_instance = base_agent.clone()

    # Ejecutar el agente con la conversación actualizada
    result = asyncio.run(Runner.run(agent_instance, conversation))
    assistant_reply = str(result.final_output)  # respuesta final del agente como texto

    # Añadir la respuesta del asistente a la conversación
    conversation.append({"role": "assistant", "content": assistant_reply})

    # Guardar la conversación actualizada en la base de datos (memoria conversacional)
    if memory_entry:
        memory_entry.messages = conversation
    else:
        memory_entry = ConversationMemory(user_id=user_id, agent_name=agent_name, messages=conversation)
        db.add(memory_entry)
    db.commit()
    db.close()

    # Devolver la respuesta (ajustar formato según necesidad, p. ej. Twilio XML o JSON)
    return jsonify({"reply": assistant_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
