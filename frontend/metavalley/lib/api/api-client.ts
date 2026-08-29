const API_URL = process.env.NEXT_PUBLIC_API_URL 

if (!API_URL) {
    throw new Error("Erro, NEXT_PUBLIC_API não configurada.");
}

type ApiOptions = RequestInit & {
  token?: string;
};

export async function apiClient<T>(
  endpoint: string,
  options: ApiOptions = {},
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers: {
      "Content-Type": "application/json",
      ...(token && {
        Authorization: `Bearer ${token}`,
      }),
      ...fetchOptions.headers,
    },
  });

  if (!response.ok) {
    throw new Error("Erro ao realizar requisição.");
  }

  return response.json();
}