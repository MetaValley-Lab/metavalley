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
