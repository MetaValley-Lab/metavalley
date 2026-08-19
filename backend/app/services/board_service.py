import asyncio
from uuid import UUID
from typing import AsyncGenerator
 
from app.agents.base.context import AgentContext, AgentMessage
from app.agents.agents import CEOAgent, CTOAgent, CFOAgent, CMOAgent
from app.agents.router import AgentRouter
from app.services.startup_service import StartupService
from app.services.canvas_zone_service import CanvasZoneService
from app.services.planning_item_service import PlanningItemService
from app.services.product_service import ProductService
from backend.app.services.action_service import ActionService
from backend.app.services.conversation_service import ConversationService
from backend.app.services.rag_service import RAGService
from backend.app.services.user_service import UserService
 


# ─────────────────────────────────────────────────────────────
# BOARD SERVICE — orquestra o chat em grupo
# ─────────────────────────────────────────────────────────────
 
class BoardService:
    """
    Orquestra o chat em grupo e individual dos agentes.
 
    Usa os services existentes do projeto (StartupService, CanvasZoneService, etc.)
    seguindo o mesmo padrão do restante da aplicação — sem repositories.
    """
 
    def __init__(self):
        self.startup_service = StartupService()
        self.canvas_service = CanvasZoneService()
        self.planning_service = PlanningItemService()
        self.product_service = ProductService()
        self.user_service = UserService()
        self.conversation_service = ConversationService()
        self.rag_service = RAGService()
        self.router = AgentRouter()
        self.action_service = ActionService(
            startup_service=self.startup_service,
            canvas_service=self.canvas_service,
            planning_service=self.planning_service,
            product_service=self.product_service,
            user_service=self.user_service,
        )
        self.agents = {
            "ceo": CEOAgent(),
            "cto": CTOAgent(),
            "cfo": CFOAgent(),
            "cmo": CMOAgent(),
        }
 
    async def process_group_message(
        self,
        message: str,
        startup_id: UUID,
        user_id: UUID,
        mode: str = "casual",
        conv_type: str = "group",
    ) -> AsyncGenerator[dict, None]:
        """
        Generator assíncrono que faz streaming das respostas dos agentes via SSE.
 
        Eventos emitidos:
        - {"event": "agent_start", "agent": "ceo"}
        - {"event": "agent_message", "agent": "ceo", "content": "...", "options": [...]}
        - {"event": "action_executed", "action_type": "update_canvas_zone", "zone": "..."}
        - {"event": "turn_complete"}
        - {"event": "error", "detail": "..."}
        """
 
        # 1. Pega ou cria a conversa (group, onboarding, ceo, etc.)
        conversation = await self.conversation_service.get_or_create_conversation(
            startup_id=str(startup_id),
            conv_type=conv_type,
        )
        conversation_id = conversation["id"]
 
        # 2. Monta o contexto completo para os agentes
        context = await self._build_context(
            message=message,
            startup_id=startup_id,
            user_id=user_id,
            conversation_id=conversation_id,
            mode=mode,
        )
 
        # 3. Seleciona quais agentes respondem
        selected_agents = self.router.select(message, mode)
 
        # 4. Salva mensagem do founder
        await self.conversation_service.save_message(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )
 
        # 5. Respostas sequenciais — cada agente vê as respostas anteriores (debate)
        all_responses: list[AgentMessage] = []
 
        for agent_name in selected_agents:
            agent = self.agents[agent_name]
            context.previous_responses = all_responses
 
            yield {"event": "agent_start", "agent": agent_name}
 
            response: AgentMessage = await agent.respond(message, context)
            all_responses.append(response)
 
            yield {
                "event": "agent_message",
                "agent": agent_name,
                "content": response.content,
                "options": response.options,
            }
 
            # Executa actions do agente
            for action in response.actions:
                result = await self.action_service.execute(
                    action=action,
                    startup_id=startup_id,
                    user_id=user_id,
                    agent_name=agent_name,
                )
                if result.get("ok"):
                    # Remove chave "ok" do evento para não poluir o frontend
                    event_data = {k: v for k, v in result.items() if k != "ok"}
                    yield {
                        "event": "action_executed",
                        "action_type": action.get("type"),
                        **event_data,
                    }
 
            # Salva resposta do agente
            await self.conversation_service.save_message(
                conversation_id=conversation_id,
                role="agent",
                content=response.content,
                agent_name=agent_name,
                actions=response.actions if response.actions else None,
            )
 
        # 6. Indexa o turno no Qdrant para RAG futuro
        await self._index_turn(message, all_responses, startup_id)
 
        yield {"event": "turn_complete"}
 
    async def _build_context(
        self,
        message: str,
        startup_id: UUID,
        user_id: UUID,
        conversation_id: str,
        mode: str,
    ) -> AgentContext:
        """
        Monta o AgentContext buscando dados em paralelo.
        Usa os services existentes — mesmo padrão do restante do projeto.
        """
        startup, canvas_list, history, retrieved_docs = await asyncio.gather(
            self.startup_service.get_startup_by_id(str(startup_id), str(user_id)),
            self.canvas_service.get_zones_by_startup(str(startup_id), str(user_id)),
            self.conversation_service.get_recent_messages(conversation_id, limit=10),
            self.rag_service.search(
                query=message,
                filter={"startup_id": str(startup_id)},
                top_k=5,
            ),
        )
 
        # Canvas como dict {zone_key: zone_data} para fácil acesso nos prompts
        canvas = {z["zone_key"]: z for z in (canvas_list or [])}
 
        # Formata documentos recuperados do Qdrant
        retrieved_context = ""
        if retrieved_docs:
            retrieved_context = "\n---\n".join([
                f"[{doc.metadata.get('date', '')}] {doc.page_content}"
                for doc in retrieved_docs
            ])
 
        return AgentContext(
            startup_id=startup_id,
            startup=startup or {},
            canvas=canvas,
            conversation_history=history,
            retrieved_context=retrieved_context,
            mode=mode,
            previous_responses=[],
        )
 
    async def _index_turn(
        self,
        user_message: str,
        responses: list[AgentMessage],
        startup_id: UUID,
    ) -> None:
        """Indexa o turno completo no Qdrant para recuperação futura via RAG."""
        for response in responses:
            chunk = f"Founder: {user_message}\n{response.agent_name.upper()}: {response.content}"
            await self.rag_service.index(
                text=chunk,
                metadata={
                    "startup_id": str(startup_id),
                    "agent_name": response.agent_name,
                    "fonte": "group_chat",
                },
            )
 
