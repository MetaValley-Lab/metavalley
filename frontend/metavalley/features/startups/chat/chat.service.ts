import { apiClient } from "@/lib/api/api-client";

export type StreamEvent =
  | { event: "agent_start"; agent: string }
  | { event: "agent_message"; agent: string; content: string; options?: unknown[] }
  | { event: "action_executed"; action_type: string; zone: string }
  | { event: "turn_complete" }
  | { event: "error"; detail: string };

export interface MessageResponse {
  id: string;
  conversation_id: string;
  role: "user" | "agent";
  agent_name?: "founder" | "ceo" | "cto" | "cfo" | "cmo" | null;
  content: string;
  actions?: unknown[] | null;
  created_at: string;
}

export interface SendMessagePayload {
  startupId: string;
  message: string;
  conversationType: string;
  mode?: string;
}

/**
 * Busca o histórico de mensagens usando o seu apiClient padrão.
 */
export async function getChatHistory(startupId: string, conversationType: string): Promise<MessageResponse[]> {
  return apiClient<MessageResponse[]>(`chat/history/${startupId}/${conversationType}`);
}

/**
 * Envia a mensagem via SSE.
 */
export async function sendMessageStream(
  payload: SendMessagePayload,
  // 1. CORRIGIDO AQUI: mudamos de 'unknown' para 'StreamEvent'
  onEvent: (event: StreamEvent) => void, 
  onError: (error: string) => void,
  onComplete: () => void
) {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  if (!API_URL) throw new Error("NEXT_PUBLIC_API_URL não configurada.");

  const baseUrl = API_URL.endsWith('/') ? API_URL : `${API_URL}/`;

  try {
    const response = await fetch(`${baseUrl}chat/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // Garante que a auth vá junto
      body: JSON.stringify({
        startup_id: payload.startupId,
        message: payload.message,
        conversation_type: payload.conversationType,
        mode: payload.mode || "casual",
      }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`Erro na requisição: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    // Loop infinito lendo os chunks (pedaços) que chegam do backend
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");

      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;

        const jsonStr = line.replace("data: ", "").trim();
        if (!jsonStr) continue;

        try {
          // 2. CORRIGIDO AQUI: Forçamos o TypeScript a entender que o JSON parseado é um StreamEvent
          const event = JSON.parse(jsonStr) as StreamEvent; 
          
          if (event.event === "error") {
            onError(event.detail);
          } else {
            onEvent(event); // Dispara callback pro frontend (agora os tipos batem)
          }
        } catch (err) {
          console.error("Falha ao ler pedaço do SSE:", err, jsonStr);
        }
      }
    }
  } catch (err: unknown) {
    onError((err as Error).message || "Erro desconhecido ao conectar com o chat.");
  } finally {
    onComplete(); // Avisa o frontend que terminou a geração
  }
}