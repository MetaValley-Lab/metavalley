export type ProductType = "saas" | "marketplace" | "app" | "hardware" | "service" | "other";
export type ProductStage = "idea" | "prototype" | "mvp" | "launched";
export type ProductActorRole = "founder" | "cto";

export interface Product {
  id: string;
  startup_id: string;
  name: string;
  description: string | null;
  type: ProductType;
  price: number | string | null;
  stage: ProductStage;
  last_updated_by: ProductActorRole;
  created_at: string;
  updated_at: string;
}

export interface CreateProductPayload {
  startup_id: string;
  name: string;
  description?: string;
  type: ProductType;
  price?: number;
  // Default no backend é "idea" — só precisa mandar se quiser outro valor.
  stage?: ProductStage;
}

