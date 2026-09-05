import { apiClient } from "@/lib/api/api-client";
import type { SimulationInterest, SimulationInterestStatus } from "./simulation.types";

export async function getMySimulationInterest(startupId: string): Promise<SimulationInterestStatus> {
  return apiClient<SimulationInterestStatus>(`/simulation-interests/startup/${startupId}/me`);
}

// O e-mail não é enviado pelo frontend — o backend usa o e-mail do usuário
// autenticado automaticamente (current_user.email).
export async function createSimulationInterest(startupId: string): Promise<SimulationInterest> {
  return apiClient<SimulationInterest>("/simulation-interests", {
    method: "POST",
    body: JSON.stringify({ startup_id: startupId }),
  });
}

export async function deleteSimulationInterest(interestId: string): Promise<void> {
  return apiClient<void>(`/simulation-interests/${interestId}`, {
    method: "DELETE",
  });
}

