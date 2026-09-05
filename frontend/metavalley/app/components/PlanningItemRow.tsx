// Local: features/planning/components/PlanningItemRow.tsx

"use client";

import { Check, Trash2 } from "lucide-react";
// import type { PlanningItem } from "../planning.types";

import type { PlanningItem } from "@/features/startups/planning/planning.types";

import { actorRoleLabels, actorRoleColors } from "@/features/startups/planning/actor-roles";

interface PlanningItemRowProps {
  item: PlanningItem;
  onToggleComplete: (item: PlanningItem) => void;
  onDelete: (item: PlanningItem) => void;
}

export default function PlanningItemRow({ item, onToggleComplete, onDelete }: PlanningItemRowProps) {
  return (
    <div className="flex items-center gap-3 border-b border-gray-100 px-3 py-3 last:border-b-0">
      <button
        type="button"
        onClick={() => onToggleComplete(item)}
        aria-label={item.completed ? "Marcar como não concluída" : "Marcar como concluída"}
        className={`flex h-5 w-5 shrink-0 cursor-pointer items-center justify-center rounded-full border-2 transition-colors ${
          item.completed ? "border-[#4735FD] bg-[#4735FD] text-white" : "border-gray-300"
        }`}
      >
        {item.completed && <Check size={12} />}
      </button>

      <p className={`flex-1 text-sm ${item.completed ? "text-gray-400 line-through" : "text-gray-900"}`}>
        {item.content}
      </p>

      {item.created_by !== "founder" && (
        <span
          className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold text-white ${actorRoleColors[item.created_by]}`}
        >
          {actorRoleLabels[item.created_by]}
        </span>
      )}

      <button
        type="button"
        onClick={() => onDelete(item)}
        aria-label="Excluir tarefa"
        className="shrink-0 cursor-pointer text-gray-300 hover:text-red-500"
      >
        <Trash2 size={16} />
      </button>
    </div>
  );
}

