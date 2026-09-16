"use client";

import { useState } from "react";
import { MoreVertical, Pencil, Rocket, Trash2 } from "lucide-react";
import type Startup from "@/features/startups/startup.types";
import Link from "next/link";

interface StartupCardProps {
  startup: Startup;
  onEdit: (startup: Startup) => void;
  onDelete: (startup: Startup) => void;
}

export default function StartupCard({ startup, onEdit, onDelete }: StartupCardProps) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="relative w-full max-w-[220px] overflow-hidden rounded-md border border-gray-200 bg-white transition hover:border-gray-300 hover:shadow-sm">
      <Link href={`/startups/${startup.id}`} className="block cursor-pointer">
        <div className="flex h-32 w-full items-center justify-center bg-gray-100">
          {startup.image_url ? (
            <img src={startup.image_url} alt={`Imagem da startup ${startup.name}`} className="h-full w-full object-cover" />
          ) : (
            <Rocket className="text-gray-400" size={32} />
          )}
        </div>
        <p className="border-t border-gray-100 p-3 text-sm font-medium text-gray-900">{startup.name}</p>
      </Link>
      <div className="absolute right-2 top-2">
        <button type="button" aria-label={`Opções de ${startup.name}`} onClick={() => setMenuOpen((open) => !open)} className="cursor-pointer rounded-full bg-white/90 p-1 text-gray-500 shadow-sm hover:text-gray-900">
          <MoreVertical size={18} />
        </button>
        {menuOpen && (
          <div className="absolute right-0 z-10 mt-1 w-32 rounded-md border border-gray-200 bg-white py-1 shadow-lg">
            <button type="button" onClick={() => onEdit(startup)} className="flex w-full cursor-pointer items-center gap-2 px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"><Pencil size={14} /> Editar</button>
            <button type="button" onClick={() => onDelete(startup)} className="flex w-full cursor-pointer items-center gap-2 px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50"><Trash2 size={14} /> Excluir</button>
          </div>
        )}
      </div>
    </div>
  );
}

