export type StartupStage = "idea" | "mvp" | "launched";

export type RevenueModel =
  | "subscription"
  | "saas"
  | "marketplace"
  | "freemium"
  | "pay_per_use"
  | "licensing"
  | "advertising"
  | "e_commerce"
  | "service"
  | "hardware"
  | "other";

export default interface Startup {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  problem: string | null;
  solution: string | null;
  segment: string | null;
  target_location: string | null;
  stage: StartupStage;
  primary_revenue_model: RevenueModel | null;
  revenue_model_details: string | null;
  // Só o valor "active" foi confirmado no exemplo de retorno; os demais
  // valores possíveis de StartupStatus não foram informados.
  status: string;
  created_at: string;
  updated_at: string;
}

