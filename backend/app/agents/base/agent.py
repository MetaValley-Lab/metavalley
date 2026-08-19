import re
import json
from abc import ABC, abstractmethod

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.base.context import AgentContext, AgentMessage


# ─────────────────────────────────────────
# INSTRUÇÕES BASE — compartilhadas por todos os agentes
# ─────────────────────────────────────────

# app/agents/base/agent.py

BASE_ACTION_INSTRUCTIONS = """
## FORMATO DE RESPOSTA OBRIGATÓRIO

Toda resposta deve seguir exatamente este formato:

[Sua mensagem natural aqui — nunca mencione os blocos técnicos abaixo]

<ACTIONS>
[array JSON de actions, ou [] se nenhuma ação necessária]
</ACTIONS>

<OPTIONS>
[array JSON de strings para botões de escolha rápida, ou [] se nenhuma]
</OPTIONS>

---

## ACTIONS DISPONÍVEIS

### Atualizar campo da startup
{
  "type": "update_startup",
  "field": "<campo>",
  "value": "<valor>"
}

Campos permitidos: name, description, problem, solution, segment,
                   target_location, stage, primary_revenue_model, revenue_model_details

Caso queria modificar o campo "stage", os únicos valores que você poderá colocar são:
- "ideia"
- "mvp"
- "launched"

Caso queira modificar o campo "primary_revenue_model", os únicos valores que você poderá colocar são:
- "subscription"
- "saas"
- "marketplace"
- "freemium"
- "pay_per_user"
- "licensing"
- "advertising"
- "e_commerce"
- "service"
- "hardware"
- "other"

### Atualizar zona do canvas vivo
{
  "type": "update_canvas_zone",
  "zone": "<zone_key>",
  "content": "<texto>",
  "status": "<status>"
  "filled_by": "<seu_nome>"
}

Como deve ser preechido o campo "zone" (apenas os valores que você pode utilizar):
- "value_proposition"
- "customer_segments"
- "acquisition_channels"
- "revenue_model"
- "cost_structure"
- "key_resource"
- "success_metrics"

Como deve ser preenchido o campo "status":
- "filled"
- "in_progress"
- "to_define"

Como você deve preencher o campo "filled_by":
- "ceo" (Se você for o CEO)
- "cto" (Se você for o CTO)
- "cfo" (Se você for o CFO)
- "cmo" (Se você for o CMO)

### Adicionar item ao planejamento
{
  "type": "add_planning_item",
  "content": "<descrição da tarefa>",
  "suggested_by": "<seu_nome>"
}

Como você deve preencher o campo "suggested_by":
- "ceo" (Se você for o CEO)
- "cto" (Se você for o CTO)
- "cfo" (Se você for o CFO)
- "cmo" (Se você for o CMO)

### Sugerir modificação de um planejamento
{
  "type": "modify_planning_item",
  "content": "<content>",
  "updated_by": "<seu_nome>"
}

Como você deve preencher o campo "updated_by":
- "ceo" (Se você for o CEO)
- "cto" (Se você for o CTO)
- "cfo" (Se você for o CFO)
- "cmo" (Se você for o CMO)

### Sugerir conclusão de tarefa (founder confirma)
{
  "type": "suggest_complete",
  "item_id": "<uuid_do_item>"
}

### Criar produto (apenas CTO em modo product_creation)
{
  "type": "create_product",
  "name": "<nome>",
  "description": "<desc>",
  "type": "<saas|marketplace|app|hardware|service|other>",
  "price": "<valor>",
  "stage": "<idea|prototype|mvp|launched>",
  "last_updated_by": "<seu_nome>"
}

Como você deve preencher o campo "last_updated_by":
- "ceo" (Se você for o CEO)
- "cto" (Se você for o CTO)
- "cfo" (Se você for o CFO)
- "cmo" (Se você for o CMO)


### Modificar produto existente
{
  "type": "create_product",
  "name": "<nome>",
  "description": "<desc>",
  "type": "<saas|marketplace|app|hardware|service|other>",
  "price": "<valor>",
  "stage": "<idea|prototype|mvp|launched>",
  "last_updated_by": "<seu_nome>"
}

Como você deve preencher o campo "last_updated_by":
- "ceo" (Se você for o CEO)
- "cto" (Se você for o CTO)
- "cfo" (Se você for o CFO)
- "cmo" (Se você for o CMO)


---

## REGRAS DE ACTIONS
1. Múltiplas actions são permitidas na lista
2. Nunca exponha os blocos <ACTIONS> ou <OPTIONS> na sua fala
3. Emita update_canvas_zone quando identificar informação relevante para o canvas
4. Emita add_planning_item quando sugerir uma próxima ação concreta ao founder
5. OPTIONS: use apenas quando a resposta esperada for de um conjunto limitado

---

## REGRAS DE DEBATE
- Você pode ver as respostas dos outros conselheiros quando elas existirem
- Quando discordar, diga explicitamente: "Discordo do [nome] porque..."
- Quando concordar e complementar: "Complementando o que o [nome] disse..."
- Não repita o que outros já disseram — adicione sua perspectiva única
"""


class BaseAgent(ABC):
    """
    Classe base para todos os agentes do MetaValley.
    Responsabilidades:
    - Construir o prompt dinamicamente com contexto rico
    - Invocar o LLM
    - Parsear a resposta (mensagem + actions + options)
    - Formatar o debate (respostas anteriores de outros agentes)
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            max_output_tokens=600,   # Controle de custo: máx 600 tokens por resposta
        )

    @abstractmethod
    def build_persona_prompt(self, context: AgentContext) -> str:
        """
        Cada agente implementa sua própria persona e especialização.
        Recebe o contexto completo para personalizar conforme necessário.
        """
        raise NotImplementedError

    async def respond(self, message: str, context: AgentContext) -> AgentMessage:
        """Pipeline completo: contexto → prompt → LLM → parsing."""
        messages = self._build_messages(message, context)
        raw_response = await self.llm.ainvoke(messages)
        
        content = raw_response.content
        if isinstance(content, list):
            raise TypeError(f"Erro, a LLM retornou uma lista inesperada: {content}")
        
        return self._parse_response(content) 

    def _build_messages(self, message: str, context: AgentContext) -> list:
        """
        Monta a lista de mensagens para o LLM:
        1. System prompt (persona + contexto da startup + instruções)
        2. Histórico de conversa (sliding window do PostgreSQL)
        3. Mensagem atual (com respostas anteriores dos outros agentes, se houver)
        """
        system_prompt = self._build_full_system_prompt(context)
        msgs: list[BaseMessage] = [SystemMessage(content=system_prompt)]

        # Sliding window: últimas 10 mensagens do histórico (controle de tokens)
        for msg in context.conversation_history[-10:]:
            role = msg.get("role")
            content = msg.get("content", "")
            agent = msg.get("agent_name", "")

            if role == "user":
                msgs.append(HumanMessage(content=content))
            elif role == "agent":
                label = f"[{agent.upper()}]" if agent else "[CONSELHEIRO]"
                msgs.append(AIMessage(content=f"{label}: {content}"))

        # Mensagem atual — com debate se outros agentes já responderam
        if context.previous_responses:
            msgs.append(HumanMessage(content=self._build_debate_message(message, context)))
        else:
            msgs.append(HumanMessage(content=message))

        return msgs

    def _build_full_system_prompt(self, context: AgentContext) -> str:
        """Combina persona + contexto da startup + canvas + instruções de ação."""
        persona = self.build_persona_prompt(context)
        startup_ctx = self._format_startup_context(context)
        rag_ctx = self._format_rag_context(context)

        return f"""{persona}

---

{startup_ctx}

{rag_ctx}

---

{BASE_ACTION_INSTRUCTIONS}
"""

    def _build_debate_message(self, message: str, context: AgentContext) -> str:
        """
        Quando outros agentes já responderam no mesmo turno,
        cada agente subsequente vê as respostas anteriores e pode debater.
        """
        previous = "\n\n".join([
            f"[{r.agent_name.upper()}]: {r.content}"
            for r in context.previous_responses
        ])

        return f"""O founder perguntou:
"{message}"

Outros conselheiros do board já responderam:

{previous}

---

Agora dê sua perspectiva como {self.agent_name.upper()}. 
Você pode concordar, discordar ou complementar. Seja direto sobre diferenças de visão.
"""

    def _parse_response(self, raw: str) -> AgentMessage:
        """
        Extrai mensagem limpa, actions e options da resposta bruta do LLM.
        Robusto a variações de formatação.
        """
        actions = self._extract_block(raw, "ACTIONS")
        options = self._extract_block(raw, "OPTIONS")

        # Remove os blocos da mensagem exibida ao usuário
        message = re.sub(r'<ACTIONS>.*?</ACTIONS>', '', raw, flags=re.DOTALL)
        message = re.sub(r'<OPTIONS>.*?</OPTIONS>', '', message, flags=re.DOTALL)
        message = message.strip()

        return AgentMessage(
            agent_name=self.agent_name,
            content=message,
            actions=actions if isinstance(actions, list) else [],
            options=options if isinstance(options, list) else [],
        )

    def _extract_block(self, raw: str, tag: str):
        """Extrai e parseia JSON de dentro de uma tag."""
        match = re.search(rf'<{tag}>\s*(.*?)\s*</{tag}>', raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return []
        return []

    @staticmethod
    def _format_startup_context(context: AgentContext) -> str:
        s = context.startup
        canvas = context.canvas

        canvas_lines = "\n".join([
            f"  - {zone}: {data.get('content', '')}"
            for zone, data in canvas.items()
        ]) if canvas else "  Nenhuma zona preenchida ainda."

        return f"""## CONTEXTO DA STARTUP DO FOUNDER

- Nome: {s.get('name', 'Não definido')}
- Problema: {s.get('problem', 'Não definido')}
- Solução: {s.get('solution', 'Não definida')}
- Segmento: {s.get('segment', 'Não definido')}
- Localização-alvo: {s.get('target_location', 'Não definida')}
- Estágio: {s.get('stage', 'Não definido')}
- Modelo de receita: {s.get('primary_revenue_model', 'Não definido')}

## CANVAS VIVO (estado atual)
{canvas_lines}"""

    @staticmethod
    def _format_rag_context(context: AgentContext) -> str:
        if not context.retrieved_context:
            return ""
        return f"""## MEMÓRIA RELEVANTE (conversas anteriores)
{context.retrieved_context}"""

