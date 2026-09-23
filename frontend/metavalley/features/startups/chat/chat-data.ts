import type { ChatContact, ChatMessage } from "./chat.types";

export const chatContacts: ChatContact[] = [
  {
    id: "group",
    name: "Board Executivo",
    description:
      "Grupo composto por CEO, CTO, CFO e CMO. Eles auxiliarão você a validar suas ideias e produtos.",
    isGroup: true,
    color: "bg-[#4735FD]",
  },
  {
    id: "ceo",
    name: "CEO",
    description:
      "Irei te ajudar a montar a sua startup com uma visão mais estratégica e pragmática",
    color: "bg-blue-500",
  },
  {
    id: "cto",
    name: "CTO",
    description: "Irei te ajudar a criar o produto ideal para o seu público",
    color: "bg-emerald-500",
  },
  {
    id: "cfo",
    name: "CFO",
    description: "Te ajudo a definir os melhores modelos de negócio e ajudo com as finanças",
    color: "bg-amber-500",
  },
  {
    id: "cmo",
    name: "CMO",
    description: "Te ajudo no marketing e fazer uma oferta irresistível para os seus clientes.",
    color: "bg-pink-500",
  },
];

export function getContactById(contactId: string): ChatContact | undefined {
  return chatContacts.find((contact) => contact.id === contactId);
}

export const initialMessages: Record<string, ChatMessage[]> = Object.fromEntries(
  chatContacts.map((contact) => [
    contact.id,
    [
      {
        id: `${contact.id}-seed`,
        contactId: contact.id,
        sender: "agent",
        content: contact.description,
        timestamp: "09:00",
      },
    ] satisfies ChatMessage[],
  ]),
);

