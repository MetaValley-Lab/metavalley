import { apiClient } from "@/lib/api/api-client";
import type { Product, CreateProductPayload } from "./product.types";

export async function getProducts(startupId: string): Promise<Product[]> {
  return apiClient<Product[]>(`/products/startup/${startupId}`);
}

export async function createProduct(payload: CreateProductPayload): Promise<Product> {
  return apiClient<Product>("/products", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateProduct(
  productId: string,
  payload: Omit<Partial<CreateProductPayload>, "startup_id">,
): Promise<Product> {
  return apiClient<Product>(`/products/${productId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteProduct(productId: string): Promise<void> {
  await apiClient<void>(`/products/${productId}`, { method: "DELETE" });
}

