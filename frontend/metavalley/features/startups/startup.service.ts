  import { apiClient } from "@/lib/api/api-client";
  import type Startup  from "./startup.types";
  import type { CreateStartupFormData } from "./startup.schema";

  export async function getStartups(): Promise<Startup[]> {
    return apiClient<Startup[]>("startups");
  }

  export async function createStartup(data: CreateStartupFormData): Promise<Startup> {
    return apiClient<Startup>("startups", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  export async function getStartup(startup_id: string): Promise<Startup> {
    return apiClient<Startup>(`startups/${startup_id}`);
  }

  export async function uploadStartupImage(startupId: string, file: File): Promise<Startup> {
    const formData = new FormData();
    formData.append("file", file);
    return apiClient<Startup>(`startups/${startupId}/image`, {
      method: "POST",
      body: formData,
    });
  }

  export async function updateStartup(
    startupId: string,
    data: CreateStartupFormData,
  ): Promise<Startup> {
    return apiClient<Startup>(`startups/${startupId}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  export async function deleteStartup(startupId: string): Promise<void> {
    await apiClient<void>(`startups/${startupId}`, { method: "DELETE" });
  }
