export interface CanvasZone {
  id: string;
  startup_id: string;
  zone_key: string;
  content: string;
  // Valores observados no exemplo: "filled", "in_progress", "to_define".
  // Outros valores podem existir e não foram confirmados.
  status: string;
  // Valores observados no exemplo: "ceo", "founder". O modelo completo do
  // board de agentes (CMO/CFO/CTO) ainda não está refletido neste endpoint.
  filled_by: string;
  updated_at: string;
  previous_content: string | null;
}

