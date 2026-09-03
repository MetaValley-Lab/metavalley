import { z } from "zod";

export const productTypeOptions = [
  { label: "SaaS", value: "saas" },
  { label: "Marketplace", value: "marketplace" },
  { label: "Aplicativo", value: "app" },
  { label: "Hardware", value: "hardware" },
  { label: "Serviço", value: "service" },
  { label: "Outro", value: "other" },
] as const;

export const productStageOptions = [
  { label: "Ideia", value: "idea" },
  { label: "Protótipo", value: "prototype" },
  { label: "MVP", value: "mvp" },
  { label: "Lançado", value: "launched" },
] as const;

export const createProductSchema = z.object({
  name: z.string().min(1, "O nome do produto é obrigatório.").max(255),
  description: z.string().optional(),
  type: z.enum(["saas", "marketplace", "app", "hardware", "service", "other"]),
  price: z
    .string()
    .optional()
    .refine((val) => !val || (!Number.isNaN(Number(val)) && Number(val) >= 0), {
      message: "Informe um preço válido (maior ou igual a zero).",
    }),
  stage: z.enum(["idea", "prototype", "mvp", "launched"]),
});

export type CreateProductFormData = z.infer<typeof createProductSchema>;

export const productSteps: { title: string; fields: (keyof CreateProductFormData)[] }[] = [
  { title: "Informações básicas", fields: ["name", "description", "type"] },
  { title: "Detalhes comerciais", fields: ["price", "stage"] },
];

