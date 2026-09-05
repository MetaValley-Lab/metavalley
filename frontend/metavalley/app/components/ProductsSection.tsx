// Local: features/products/components/ProductsSection.tsx

"use client";

import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { deleteProduct, getProducts } from "@/features/startups/products/product.service";
import type { Product } from "@/features/startups/products/product.types";
import ProductCard from "./ProductCard";
import CreateProductModal from "./CreateProductModal";
import ConfirmModal from "./ConfirmModal";

interface ProductsSectionProps {
  startupId: string;
}

export default function ProductsSection({ startupId }: ProductsSectionProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [deletingProduct, setDeletingProduct] = useState<Product | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    async function loadProducts() {
      setLoading(true);
      setError(null);
      try {
        const data = await getProducts(startupId);
        setProducts(data);
      } catch {
        setError("Não foi possível carregar os produtos agora.");
      } finally {
        setLoading(false);
      }
    }
    loadProducts();
  }, [startupId, refreshKey]);

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Seus produtos</h2>
        <button
          type="button"
          onClick={() => setModalOpen(true)}
          className="flex cursor-pointer items-center gap-1.5 rounded-full bg-[#4735FD] px-4 py-2 text-sm font-semibold text-white hover:bg-[#3c2ce0]"
        >
          <Plus size={16} />
          Criar novo produto
        </button>
      </div>

      {loading ? (
        <div className="h-40 w-full animate-pulse rounded-md bg-gray-100" />
      ) : error ? (
        <p className="text-sm text-red-500">{error}</p>
      ) : products.length === 0 ? (
        <p className="text-sm text-gray-400">Nenhum produto criado ainda.</p>
      ) : (
        <div className="flex flex-wrap gap-4">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onEdit={(item) => { setEditingProduct(item); setModalOpen(true); }}
              onDelete={setDeletingProduct}
            />
          ))}
        </div>
      )}

      <CreateProductModal
        startupId={startupId}
        visible={modalOpen}
        product={editingProduct}
        onHide={() => { setModalOpen(false); setEditingProduct(null); }}
        onCreated={() => {
          setModalOpen(false);
          setEditingProduct(null);
          setRefreshKey((k) => k + 1);
        }}
      />
      <ConfirmModal
        visible={Boolean(deletingProduct)}
        title="Excluir produto"
        message={`Tem certeza que deseja excluir o produto "${deletingProduct?.name ?? ""}"?`}
        isSubmitting={deleting}
        onHide={() => setDeletingProduct(null)}
        onConfirm={async () => {
          if (!deletingProduct) return;
          setDeleting(true);
          try {
            await deleteProduct(deletingProduct.id);
            setDeletingProduct(null);
            setRefreshKey((key) => key + 1);
          } finally {
            setDeleting(false);
          }
        }}
      />
    </section>
  );
}

