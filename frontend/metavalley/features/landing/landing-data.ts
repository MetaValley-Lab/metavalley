import type { ComponentType } from "react";
import { icons } from "./landing-icons";

export type LandingIcon = ComponentType<{ size?: number }>;

export type Agent = {
  name: string;
  role: string;
  color: string;
  question: string;
};

export type ColorItem = {
  title: string;
  description: string;
  icon: LandingIcon;
  color: string;
};

export const agents: Agent[] = [
  { name: "CEO", role: "Estratégia", color: "#7F77DD", question: "Qual o CAC estimado no seu modelo?" },
  { name: "CTO", role: "Tecnologia", color: "#0891B2", question: "Como você pretende construir isso?" },
  { name: "CFO", role: "Finanças", color: "#22C55E", question: "Qual sua margem e runway?" },
  { name: "CMO", role: "Marketing", color: "#F43F5E", question: "Quem compraria isso primeiro?" },
];

export const brands = ["Ada Metaverse", "InovaTech", "StartupNE", "Centelha Program"];

export const problems: ColorItem[] = [
  { title: "Meses perdidos construindo o produto errado", description: "Sem validação, founders passam semanas ou meses desenvolvendo features que nenhum usuário pediu.", icon: icons.clock, color: "#7F77DD" },
  { title: "Pesquisa de mercado é cara e lenta demais", description: "Consultorias custam caro e pesquisas com usuários reais podem levar meses.", icon: icons.chartDown, color: "#F43F5E" },
  { title: "Opinião de mentor não é dado", description: "Todo fundador já ouviu que sua ideia era incrível. Depois descobriu que ninguém pagaria por ela.", icon: icons.bulb, color: "#22C55E" },
];

export const features: ColorItem[] = [
  { title: "Board de Agentes IA", description: "CEO, CTO, CFO e CMO com personalidades e visões distintas.", icon: icons.brain, color: "#7F77DD" },
  { title: "Chat em Grupo e Individual", description: "Debata com o board ou converse em privado com um conselheiro.", icon: icons.users, color: "#0891B2" },
  { title: "Canvas Vivo", description: "Seu modelo de negócio é preenchido automaticamente pelas conversas.", icon: icons.grid, color: "#22C55E" },
  { title: "Planejamento Inteligente", description: "Receba próximas ações baseadas no que o board descobriu.", icon: icons.rocket, color: "#F59E0B" },
  { title: "Simulação de Mercado", description: "Dados sintéticos de validação antes do produto existir.", icon: icons.chartDown, color: "#7F77DD" },
  { title: "Histórico e Memória", description: "Os agentes lembram das decisões e discussões da sua startup.", icon: icons.message, color: "#EC4899" },
];

export const steps = [
  ["01", "Descreva sua ideia naturalmente", "Sem formulários. Converse com o CEO Agent como faria com um conselheiro de confiança."],
  ["02", "Consulte o board executivo", "CEO, CTO, CFO e CMO debatem sua ideia com perspectivas reais e conflitantes."],
  ["03", "Veja seu canvas tomar forma", "As conversas preenchem automaticamente seu Business Model Canvas."],
  ["04", "Construa com dados", "Execute uma simulação de mercado sintético antes de investir um centavo."],
] as const;

export const plans = {
  free: ["Board de agentes — 50 msg/mês", "Canvas vivo", "1 startup", "2 produtos"],
  pro: ["Board ilimitado", "Canvas ilimitado", "Simulação TME — pay-per-use", "3 startups", "Histórico completo"],
};
