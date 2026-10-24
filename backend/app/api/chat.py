import json
from typing import List
from uuid import UUID
from supabase.client import Client

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse
from supabase_auth import User

from app.api.dependencies import get_current_user
from app.services.board_service import BoardService
from app.schemas.chat_schema import (
    MessageRequest,
    ConversationResponse,
    ConversationType,
    MessageResponse
)
from app.core.supabase import get_supabase_client

from app.services.board_service import BoardService
from app.services.conversation_service import ConversationService


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/message",
    summary="Envia mensagem ao board de agentes — resposta via Server-Sent Events (SSE)"
)
async def send_message(
    request: Request,
    payload: MessageRequest,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    """
    Envia uma mensagem e recebe as respostas dos agentes em streaming via SSE.

    Como consumir no frontend:
    ```js
    const response = await fetch('/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ startup_id, message, mode, conversation_type }),
        credentials: 'include',  // envia o cookie de auth
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const lines = decoder.decode(value).split('\\n');
        for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const event = JSON.parse(line.replace('data: ', ''));

            if (event.event === 'agent_message') {
                // Exibe mensagem do agente: event.agent, event.content, event.options
            }
            if (event.event === 'action_executed') {
                // Atualiza canvas, planning, etc.: event.action_type, event.zone, ...
            }
            if (event.event === 'turn_complete') {
                // Todos os agentes responderam
            }
            if (event.event === 'error') {
                // Trata erro: event.detail
            }
        }
    }
    ```

    Eventos emitidos (em ordem):
    - `agent_start`:      {"event": "agent_start", "agent": "ceo"}
    - `agent_message`:    {"event": "agent_message", "agent": "ceo", "content": "...", "options": [...]}
    - `action_executed`:  {"event": "action_executed", "action_type": "update_canvas_zone", "zone": "..."}
    - `turn_complete`:    {"event": "turn_complete"}
    - `error`:            {"event": "error", "detail": "..."}
    """

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)

    async def generate():
        try:
            board_service = BoardService(supabase_client)
            async for event in board_service.process_group_message(
                message=payload.message,
                startup_id=payload.startup_id,
                user_id=UUID(str(current_user.id)),
                mode=payload.mode,
                conv_type=payload.conversation_type,
            ):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

        except Exception as e:
            error_event = {"event": "error", "detail": str(e)}
            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Desabilita buffer do Nginx para SSE funcionar corretamente
        },
    )
    
    

@router.get(
    "/history/{startup_id}/{conversation_type}",
    response_model=List[MessageResponse],
    summary="Retorna o histórico de mensagens de uma conversa",
)
async def get_message_history(
    request: Request,
    startup_id: UUID,
    conversation_type: ConversationType,
    limit: int = Query(default=100, ge=1, le=500, description="Máximo de mensagens retornadas"),
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    """
    Retorna as mensagens de uma conversa específica em ordem cronológica.
 
    - `conversation_type`: `group` | `onboarding` | `ceo` | `cto` | `cfo` | `cmo`
    - Se a conversa ainda não existe, retorna lista vazia `[]`.
    - As mensagens incluem tanto as do founder (`role: user`) quanto as dos agentes (`role: agent`).
 
    Uso típico no frontend: ao abrir qualquer chat (grupo ou individual),
    chame este endpoint para carregar o histórico antes de exibir o input.
    """
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    conversation_service = ConversationService(supabase_client)
    
    messages = await conversation_service.get_messages_by_startup_and_type(
        startup_id=str(startup_id),
        conv_type=conversation_type.value,
        limit=limit,
    )
 
    return messages
 
 
# ─── GET — conversas da startup ────────────────────────────────────────────────
 
@router.get(
    "/conversations/{startup_id}",
    response_model=List[ConversationResponse],
    summary="Lista todas as conversas de uma startup",
)
async def get_conversations(
    request: Request,
    startup_id: UUID,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    """
    Lista todas as conversas que já existem para a startup.
 
    Uma conversa é criada automaticamente na primeira mensagem enviada
    para aquele tipo de chat. Antes disso, o tipo não aparece aqui.
 
    Uso típico no frontend: ao abrir o painel de chat, chame este endpoint
    para exibir indicadores visuais nos chats que já têm histórico
    (ex: badge de "N mensagens" no ícone do CEO, CTO, etc.).
    """
        
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    conversation_service = ConversationService(supabase_client)
    
    conversations = await conversation_service.get_conversations_by_startup(
        startup_id=str(startup_id),
    )
 
    return conversations
    