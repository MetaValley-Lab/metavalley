import { apiClient } from "@/lib/api/api-client";
import type { CanvasZone } from "./canvas.types";

export async function getCanvasZones(startupId: string): Promise<CanvasZone[]> {
  return apiClient<CanvasZone[]>(`/canvas-zones/startup/${startupId}`);
}