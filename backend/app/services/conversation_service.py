from typing import Any, Dict, List, Optional, cast
from app.core.supabase import supabase


class ConversationService:
    """
    Gerencia conversas e mensagens.
    Cada startup tem uma conversa por tipo (group, onboarding, ceo, cto, cfo, cmo).
    As mensagens são a fonte da verdade do histórico de chat (PostgreSQL).
    O Qdrant armazena embeddings para busca semântica (RAG) — propósito diferente.
    """

    async def get_or_create_conversation(
        self,
        startup_id: str,
        conv_type: str,
    ) -> Dict[str, Any]:
        """
        Retorna a conversa existente ou cria uma nova.
        Cada (startup_id, type) é único — constraint no banco.
        """
        response = (
            supabase.table("conversations")
            .select("*")
            .eq("startup_id", startup_id)
            .eq("type", conv_type)
            .limit(1)
            .execute()
        )

        if response.data:
            return cast(Dict[str, Any], response.data[0])

        # Cria nova conversa
        insert_response = (
            supabase.table("conversations")
            .insert({"startup_id": startup_id, "type": conv_type})
            .execute()
        )

        if not insert_response.data:
            raise Exception("Erro ao criar conversa.")

        return cast(Dict[str, Any], insert_response.data[0])

    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        agent_name: Optional[str] = None,
        actions: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Salva uma mensagem (do founder ou de um agente) no banco.
        """
        data: Dict[str, Any] = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
        }

        if agent_name:
            data["agent_name"] = agent_name

        if actions:
            data["actions"] = actions  # Supabase aceita Python list → JSONB

        response = supabase.table("messages").insert(data).execute()

        if not response.data:
            raise Exception("Erro ao salvar mensagem.")

        return cast(Dict[str, Any], response.data[0])

    async def get_recent_messages(
        self,
        conversation_id: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Retorna as últimas N mensagens em ordem cronológica.
        Usado para montar o sliding window do contexto dos agentes.
        """
        # Busca as mais recentes primeiro, depois inverte para ordem cronológica
        response = (
            supabase.table("messages")
            .select("id, role, agent_name, content, created_at")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        messages = response.data or []
        return cast(list[dict[str, Any]], list(reversed(messages)))  # Mais antigas primeiro → contexto correto para o LLM


    async def get_messages_by_startup_and_type(
        self,
        startup_id: str, 
        conv_type: str, 
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Retorna o histórico completo de mensagens de uma conversa específica.
        Usado pelo endpoint GET /chat/history/{startup_id}/{conversation_type}.
 
        Se a conversa ainda não existe, retorna lista vazia —
        o frontend interpreta isso como chat sem histórico ainda.
        
        """
        conv_response = (
            supabase.table("conversations")
            .select("id")
            .eq("startup_id", startup_id)
            .eq("type", conv_type)
            .limit(1)
            .execute()
        )
 
        if not conv_response.data:
            return []
 
        conversation_id = conv_response.data[0]["id"]
 
        messages_response = (
            supabase.table("messages")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=False)
            .limit(limit)
            .execute()
        )
 
        return cast(List[Dict[str, Any]], messages_response.data or [])
 
    async def get_conversations_by_startup(
        self,
        startup_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Lista todas as conversas que existem para uma startup.
        Útil para o frontend saber quais chats já possuem histórico.
        """
        response = (
            supabase.table("conversations")
            .select("*")
            .eq("startup_id", startup_id)
            .order("created_at", desc=False)
            .execute()
        )
 
        return cast(List[Dict[str, Any]], response.data or [])

    