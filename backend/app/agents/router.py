AGENT_KEYWORDS: dict[str, list[str]] = {
    "cfo": [
        "preço", "custo", "receita", "financeiro", "runway", "cac", "ltv",
        "investimento", "capital", "margem", "lucro", "burn", "salário",
        "orçamento", "precificação", "valuation", "equity", "dinheiro", "caixa",
    ],
    "cto": [
        "tecnologia", "stack", "arquitetura", "banco", "api", "backend",
        "frontend", "deploy", "código", "sistema", "infra", "segurança",
        "produto", "feature", "bug", "mvp técnico", "linguagem", "framework",
        "programação", "desenvolvimento", "servidor", "dados",
    ],
    "cmo": [
        "marketing", "canal", "cliente", "aquisição", "anúncio", "copy",
        "posicionamento", "branding", "conteúdo", "tráfego", "conversão",
        "funil", "redes sociais", "campanha", "seo", "growth", "icp",
        "persona", "go-to-market", "lançamento", "divulgação",
    ],
}
 
 
class AgentRouter:
    """
    Seleciona quais agentes respondem e define a ordem.
    CEO sempre participa. Especialistas entram quando o tema é relevante.
    Máximo 3 agentes por turno.
    """
 
    def select(self, message: str, mode: str = "casual") -> list[str]:
        message_lower = message.lower()
        selected = ["ceo"]
 
        for agent_name, keywords in AGENT_KEYWORDS.items():
            if any(kw in message_lower for kw in keywords):
                selected.append(agent_name)
 
        # Ordem: CEO → CFO → CTO → CMO
        order = ["ceo", "cfo", "cto", "cmo"]
        return [a for a in order if a in selected][:3]
