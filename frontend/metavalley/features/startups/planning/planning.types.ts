export type ActorRole = "founder" | "ceo" | "cto" | "cfo" | "cmo";

export interface PlanningItem {
  id: string;
  startup_id: string;
  content: string;
  created_by: ActorRole;
  last_updated_by: ActorRole;
  completed: boolean;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreatePlanningItemPayload {
  startup_id: string;
  content: string;
  // Default no backend é "founder" — só precisa mandar se for outro ator.
  created_by?: ActorRole;
}

export interface UpdatePlanningItemPayload {
  content?: string;
  completed?: boolean;
  // Default no backend é "founder" — só precisa mandar se for outro ator.
  updated_by?: ActorRole;
}

