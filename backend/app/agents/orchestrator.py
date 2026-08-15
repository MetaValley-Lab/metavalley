# Orquestrador será responsável por controlar o fluxo do motor RAG e decidir quais agentes serão acionados
from app.agents.ceo_agent import CEOAgent
from app.agents.cto_agent import CTOAgent


chain_agents: dict = {
        "ceo_agent": CEOAgent(),
        "cto_agent": CTOAgent()
    }
