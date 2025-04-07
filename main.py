import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from agents_setup import AGENTS
from supabase_client import get_conversation_memory, save_conversation_memory
from agents import Runner


app = FastAPI()

class WebhookPayload(BaseModel):
    user_id: str | None = None
    From: str | None = None
    message: str | None = None
    Body: str | None = None
    agent: str | None = "assistant"

@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    # Obtener datos del mensaje entrante
    user_id = payload.user_id or payload.From
    message_text = payload.message or payload.Body
    agent_name = payload.agent or "assistant"

    if not user_id or not message_text:
        return JSONResponse(content={"error": "user_id o message faltante"}, status_code=400)

    if agent_name not in AGENTS:
        agent_name = "assistant"

    # Obtener el historial de conversación desde Supabase
    memory_entry = get_conversation_memory(user_id, agent_name)
    conversation = list(memory_entry['messages']) if memory_entry and memory_entry.get('messages') else []
    conversation.append({"role": "user", "content": message_text})

    base_agent = AGENTS[agent_name]
    agent_instance = base_agent.clone()

    result = await Runner.run(agent_instance, conversation)
    assistant_reply = str(result.final_output)
    conversation = result.to_input_list()

    # Guardar el historial actualizado en Supabase
    save_conversation_memory(user_id, agent_name, conversation)

    return {"reply": assistant_reply}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5050))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
