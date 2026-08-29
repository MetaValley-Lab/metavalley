import { z } from "zod";

export const stageOptions = [
  { label: "Ideia", value: "idea" },
  { label: "MVP", value: "mvp" },
  { label: "Lançada", value: "launched" },
] as const;

export const revenueModelOptions = [
  { label: "Assinatura", value: "subscription" },
  { label: "SaaS", value: "saas" },
  { label: "Marketplace", value: "marketplace" },
  { label: "Freemium", value: "freemium" },
  { label: "Pagamento por uso", value: "pay_per_use" },
  { label: "Licenciamento", value: "licensing" },
  { label: "Publicidade", value: "advertising" },
  { label: "E-commerce", value: "e_commerce" },
  { label: "Serviço", value: "service" },
  { label: "Hardware", value: "hardware" },
  { label: "Outro", value: "other" },
] as const;

export const createStartupSchema = z.object({
  name: z.string().min(1, "O nome da startup é obrigatório.").max(255),
  description: z.string().optional(),
  problem: z.string().optional(),
  solution: z.string().optional(),
  segment: z.string().max(255).optional(),
  target_location: z.string().max(255).optional(),
  stage: z.enum(["idea", "mvp", "launched"]),
  primary_revenue_model: z
    .enum([
      "subscription",
      "saas",
      "marketplace",
      "freemium",
      "pay_per_use",
      "licensing",
      "advertising",
      "e_commerce",
      "service",
      "hardware",
      "other",
    ])
    .optional(),
  revenue_model_details: z.string().optional(),
});

export type CreateStartupFormData = z.infer<typeof createStartupSchema>;

export const startupSteps: { title: string; fields: (keyof CreateStartupFormData)[] }[] = [
  { title: "Informações básicas", fields: ["name", "description", "target_location"] },
  { title: "Problema e solução", fields: ["problem", "solution"] },
  {
    title: "Modelo de negócio",
    fields: ["segment", "stage", "primary_revenue_model", "revenue_model_details"],
  },
];

