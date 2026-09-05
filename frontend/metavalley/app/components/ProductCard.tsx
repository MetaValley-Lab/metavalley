"use client";

import { useState } from "react";
import { MoreVertical, Package, Pencil, Trash2 } from "lucide-react";
import type { Product } from "@/features/startups/products/product.types";

interface ProductCardProps {
  product: Product;
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
}

export default function ProductCard({ product, onEdit, onDelete }: ProductCardProps) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="relative w-full max-w-[220px] overflow-hidden rounded-md border border-gray-200 bg-white">
      <div className="flex h-32 w-full items-center justify-center bg-gray-100">
        {/* TODO: trocar por <Image> com a foto do produto quando o upload estiver disponível */}
        <Package className="text-gray-400" size={32} />
      </div>
      <p className="border-t border-gray-100 p-3 text-sm font-medium text-gray-900">
        {product.name}
      </p>
      <div className="absolute right-2 top-2">
        <button type="button" aria-label={`Opções de ${product.name}`} onClick={() => setMenuOpen((open) => !open)} className="cursor-pointer rounded-full bg-white/90 p-1 text-gray-500 shadow-sm hover:text-gray-900"><MoreVertical size={18} /></button>
        {menuOpen && (
          <div className="absolute right-0 z-10 mt-1 w-32 rounded-md border border-gray-200 bg-white py-1 shadow-lg">
            <button type="button" onClick={() => onEdit(product)} className="flex w-full cursor-pointer items-center gap-2 px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"><Pencil size={14} /> Editar</button>
            <button type="button" onClick={() => onDelete(product)} className="flex w-full cursor-pointer items-center gap-2 px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50"><Trash2 size={14} /> Excluir</button>
          </div>
        )}
      </div>
    </div>
  );
}

