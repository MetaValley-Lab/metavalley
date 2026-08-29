"use client";

import { useState } from "react";
import { PanelLeftClose, PanelLeftOpen, Search, Plus } from "lucide-react";

const navItems = [
  { icon: Search, label: "Buscar" },
  { icon: Plus, label: "Criar" },
];

export default function Sidebar() {
  const [expanded, setExpanded] = useState(false);

  return (
    <aside
      className={`flex h-screen shrink-0 flex-col justify-between border-r border-gray-200 bg-gray-50 py-4 transition-all ${
        expanded ? "w-56" : "w-14"
      }`}
    >
      <div className="flex flex-col gap-1 px-3">
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          aria-label={expanded ? "Recolher menu" : "Expandir menu"}
          className="cursor-pointer flex items-center gap-3 rounded-md p-2 text-gray-500 hover:bg-gray-200"
        >
          {expanded ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
        </button>

        {navItems.map(({ icon: Icon, label }) => (
          <button
            key={label}
            type="button"
            className="cursor-pointer flex items-center gap-3 rounded-md p-2 text-gray-500 hover:bg-gray-200"
          >
            <Icon size={20} className="shrink-0" />
            {expanded && <span className="text-sm">{label}</span>}
          </button>
        ))}
      </div>

      <div className="px-3">
        <div className="h-8 w-8 shrink-0 rounded-full bg-gray-300" />
        {/* TODO: trocar pela foto real do usuário quando o perfil estiver disponível */}
      </div>
    </aside>
  );
}

