export interface Product {
  id: string;
  startup_id: string;
  name: string;
  description: string | null;
  // Enum ProductType não foi detalhado; valores possíveis não confirmados.
  type: string;
  price: number | string | null;
  // Enum ProductStage não foi detalhado; valores possíveis não confirmados.
  stage: string;
  // Enum ProductActorRole não foi detalhado; valores possíveis não confirmados.
  last_updated_by: string;
  created_at: string;
  updated_at: string;
}

