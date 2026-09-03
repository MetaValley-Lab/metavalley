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

