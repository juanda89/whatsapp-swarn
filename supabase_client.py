from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)

def get_conversation_memory(user_id: str, agent_name: str):
    """Obtener el historial de conversación de un usuario con un agente específico"""
    response = supabase.table('conversation_memories') \
        .select('*') \
        .eq('user_id', user_id) \
        .eq('agent_name', agent_name) \
        .execute()
    
    return response.data[0] if response.data else None

def save_conversation_memory(user_id: str, agent_name: str, messages: list):
    """Guardar o actualizar el historial de conversación"""
    existing = get_conversation_memory(user_id, agent_name)
    
    if existing:
        # Actualizar registro existente
        response = supabase.table('conversation_memories') \
            .update({'messages': messages}) \
            .eq('id', existing['id']) \
            .execute()
    else:
        # Crear nuevo registro
        response = supabase.table('conversation_memories') \
            .insert({
                'user_id': user_id,
                'agent_name': agent_name,
                'messages': messages
            }) \
            .execute()
    
    return response.data[0] if response.data else None 