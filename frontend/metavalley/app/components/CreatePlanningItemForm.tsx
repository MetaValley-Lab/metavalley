// Local: features/planning/components/CreatePlanningItemForm.tsx

"use client";

import { useState, type FormEvent } from "react";
import { Plus } from "lucide-react";

interface CreatePlanningItemFormProps {
  onCreate: (content: string) => void;
  creating: boolean;
}

export default function CreatePlanningItemForm({ onCreate, creating }: CreatePlanningItemFormProps) {
  const [value, setValue] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    onCreate(trimmed);
    setValue("");
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 border-b border-gray-200 p-3">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Adicionar uma nova tarefa"
        className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-[#4735FD] focus:outline-none focus:ring-2 focus:ring-[#4735FD]/30"
      />
      <button
        type="submit"
        disabled={!value.trim() || creating}
        className="flex shrink-0 cursor-pointer items-center gap-1.5 rounded-md bg-[#4735FD] px-3 py-2 text-sm font-semibold text-white hover:bg-[#3c2ce0] disabled:cursor-not-allowed disabled:opacity-50"
      >
        <Plus size={16} />
        Adicionar
      </button>
    </form>
  );
}


