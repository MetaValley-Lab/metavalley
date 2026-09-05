import type { ActorRole } from "./planning.types";

export const actorRoleLabels: Record<ActorRole, string> = {
  founder: "Você",
  ceo: "CEO",
  cto: "CTO",
  cfo: "CFO",
  cmo: "CMO",
};

export const actorRoleColors: Record<ActorRole, string> = {
  founder: "bg-gray-400",
  ceo: "bg-blue-500",
  cto: "bg-emerald-500",
  cfo: "bg-amber-500",
  cmo: "bg-pink-500",
};

