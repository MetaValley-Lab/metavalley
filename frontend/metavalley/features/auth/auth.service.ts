import { apiClient } from "@/lib/api/api-client";
import type {LoginResponse, LoginRequest, RegisterResponse } from "./auth.types";
import { RegisterRequest } from "./auth.schema";

interface AuthMessageResponse {
  message: string;
}

export async function login(
  data: LoginRequest,
): Promise<LoginResponse> {
  return apiClient<LoginResponse>("auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}


export async function register(
  data: RegisterRequest,
): Promise<RegisterResponse> {
  return apiClient<RegisterResponse>("auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function requestPasswordReset(email: string): Promise<AuthMessageResponse> {
  return apiClient<AuthMessageResponse>("auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function resetPassword(
  credentials: { code?: string; accessToken?: string; refreshToken?: string },
  newPassword: string,
): Promise<AuthMessageResponse> {
  return apiClient<AuthMessageResponse>("auth/reset-password", {
    method: "POST",
    body: JSON.stringify({
      code: credentials.code,
      access_token: credentials.accessToken,
      refresh_token: credentials.refreshToken,
      new_password: newPassword,
    }),
  });
}
