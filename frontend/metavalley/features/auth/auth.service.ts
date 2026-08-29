import { apiClient } from "@/lib/api/api-client";
import type {LoginResponse, LoginRequest, RegisterResponse } from "./auth.types";
import { RegisterRequest } from "./auth.schema";

export async function login(
  data: LoginRequest,
): Promise<LoginResponse> {
  return apiClient<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}


export async function register(
  data: RegisterRequest,
): Promise<RegisterResponse> {
  return apiClient<RegisterResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
