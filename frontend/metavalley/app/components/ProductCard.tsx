import { Package } from "lucide-react";
import type { Product } from "@/features/startups/products/product.types";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="w-full max-w-[220px] overflow-hidden rounded-md border border-gray-200 bg-white">
      <div className="flex h-32 w-full items-center justify-center bg-gray-100">
        {/* TODO: trocar por <Image> com a foto do produto quando o upload estiver disponível */}
        <Package className="text-gray-400" size={32} />
      </div>
      <p className="border-t border-gray-100 p-3 text-sm font-medium text-gray-900">
        {product.name}
      </p>
    </div>
  );
}

