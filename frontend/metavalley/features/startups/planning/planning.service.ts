import { apiClient } from "@/lib/api/api-client";
// import type { PlanningItem, CreatePlanningItemPayload, UpdatePlanningItemPayload } from "./planning.types";
import type { PlanningItem, CreatePlanningItemPayload, UpdatePlanningItemPayload } from "./planning.types";

export async function getPlanningItems(startupId: string): Promise<PlanningItem[]> {
  return apiClient<PlanningItem[]>(`/planning-items/startup/${startupId}`);
}

export async function createPlanningItem(payload: CreatePlanningItemPayload): Promise<PlanningItem> {
  return apiClient<PlanningItem>("/planning-items", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updatePlanningItem(
  itemId: string,
  payload: UpdatePlanningItemPayload,
): Promise<PlanningItem> {
  return apiClient<PlanningItem>(`/planning-items/${itemId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deletePlanningItem(itemId: string): Promise<void> {
  return apiClient<void>(`/planning-items/${itemId}`, {
    method: "DELETE",
  });
}

