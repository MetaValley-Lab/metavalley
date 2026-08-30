import { apiClient } from "@/lib/api/api-client";
import type { Product } from "./product.types";

export async function getProducts(startupId: string): Promise<Product[]> {
  return apiClient<Product[]>(`/products/startup/${startupId}`);
}