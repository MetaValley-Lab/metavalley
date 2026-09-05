// Ordem de exibição do canvas, seguindo o layout de referência.
export const canvasZoneOrder = [
  "value_proposition",
  "customer_segments",
  "acquisition_channels",
  "revenue_model",
  "cost_structure",
  "key_resource",
  "success_metrics",
] as const;

export const canvasZoneTitles: Record<string, string> = {
  value_proposition: "Proposta de Valor",
  customer_segments: "Segmento de Clientes",
  acquisition_channels: "Canais de Aquisição",
  revenue_model: "Modelo de Receita",
  cost_structure: "Estrutura de Custos",
  key_resource: "Recursos-Chave",
  success_metrics: "Métricas de Sucesso",
};

export const canvasZoneEmptyText: Record<string, string> = {
  value_proposition: "Proposta de valor ainda não definida.",
  customer_segments: "Segmento de clientes ainda não definido.",
  acquisition_channels: "Canais de aquisição ainda não definidos.",
  revenue_model: "Modelo de receita ainda não definido.",
  cost_structure: "Estrutura de custos ainda não definida.",
  key_resource: "Recursos-chave ainda não definidos.",
  success_metrics: "Métricas de sucesso ainda não definidas.",
};

export const filledByLabels: Record<string, string> = {
  ceo: "CEO",
  founder: "Founder",
};

