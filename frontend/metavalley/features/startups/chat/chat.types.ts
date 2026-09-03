export interface ChatContact {
  id: string; // "group" | "ceo" | "cto" | "cfo" | "cmo"
  name: string;
  description: string;
  isGroup?: boolean;
  color: string;
}

export interface ChatMessage {
  id: string;
  contactId: string;
  sender: "user" | "agent"; // Backend usa MessageRole: "user" | "agent"
  agentName?: string | null; // Adicionado para saber qual agente respondeu no grupo
  content: string;
  timestamp: string; 
}