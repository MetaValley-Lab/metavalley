const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("Erro, NEXT_PUBLIC_API não configurada.");
}

type ApiOptions = RequestInit & {
  token?: string;
};

export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

export async function apiClient<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
  const { token, ...fetchOptions } = options;

  if(!API_URL) {
    throw new Error("Erro, NEXT_PUBLIC_API não configurada.");
  }

  console.log(API_URL);
  
  const baseUrl = API_URL.endsWith('/') ? API_URL : `${API_URL}/`; 
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  const fullUrl = `${baseUrl}${cleanEndpoint}`;

  const response = await fetch(fullUrl, {
    ...fetchOptions,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...fetchOptions.headers,
    },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail =
      body && typeof body === "object" && "detail" in body ? String(body.detail) : null;
    throw new ApiError(detail ?? "Erro ao realizar requisição.", response.status, body);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}
