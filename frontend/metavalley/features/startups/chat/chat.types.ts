
export interface ChatContact {
  id: string;
  name: string;
  description: string;
  isGroup?: boolean;
  // Classe Tailwind de fundo do avatar (usada até existir foto real).
  color: string;
}

export interface ChatMessage {
  id: string;
  contactId: string;
  sender: "user" | "contact";
  content: string;
  timestamp: string;
}