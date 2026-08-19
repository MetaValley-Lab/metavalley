from dataclasses import dataclass, field
from uuid import UUID

@dataclass
class AgentMessage:
  """Resposta de um agente após o parsen"""
  agent_name: str                                     # "ceo", "cto", "cfo", "cmo"
  content: str                                        # Conteúdo da mensagem do agente
  actions: list[dict] = field(default_factory=list)   # Actions a serem executadas no sistema
  options: list[str] = field(default_factory=list)    # Qucik reply buttons para o frontend


@dataclass
class AgentContext:
  """
  Contexto completo injetado em cada agente a cada turno.
  É o que diferencia nossso agentes de uma LLM genéria.
  """
  startup_id: UUID
  startup: dict                                                            # Dados da tabela de startup
  canvas: dict                                                             # Zona preenchida do canvas vivo
  conversation_history: list[dict] = field(default_factory=list)           # Últimas N mensagens do PostegreSQL
  retrieved_context: str = ""                                              # Contexto recuperado pelo Qdrant
  mode: str = "casual"                                                     # Para o CTO: "casual" | "product_creation"
  previous_responses: list[AgentMessage] = field(default_factory=list)     # Respostas anteriores dos outros agentes
  
  