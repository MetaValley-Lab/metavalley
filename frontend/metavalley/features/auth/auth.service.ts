import { apiClient } from "@/lib/api/api-client";
import type {LoginResponse, LoginRequest} from "./auth.types";

export async function login(
  data: LoginRequest,
): Promise<LoginResponse> {
  return apiClient<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}