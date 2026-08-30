// Local: features/chat/components/ChatLayout.tsx

"use client";

import { useState } from "react";
import { chatContacts, initialMessages } from "@/features/startups/chat/chat-data";
import type { ChatMessage } from "@/features/startups/chat/chat.types";
import ContactsSidebar from "@/app/components/ContactsSidebar";
import ConversationView from "@/app/components/ConversationView";

export default function ChatLayout() {
  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);
  const [messagesByContact, setMessagesByContact] =
    useState<Record<string, ChatMessage[]>>(initialMessages);

  const selectedContact = chatContacts.find((c) => c.id === selectedContactId) ?? null;

  function handleSend(content: string) {
    if (!selectedContactId) return;

    const newMessage: ChatMessage = {
      id: `${selectedContactId}-${Date.now()}`,
      contactId: selectedContactId,
      sender: "user",
      content,
      timestamp: new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
    };

    setMessagesByContact((prev) => ({
      ...prev,
      [selectedContactId]: [...(prev[selectedContactId] ?? []), newMessage],
    }));
    // TODO: enviar a mensagem para o backend/IA quando essa integração existir.
    // Por enquanto ela só fica no estado local do componente (sem persistência).
  }

  function lastMessagePreview(contactId: string): string {
    const contactMessages = messagesByContact[contactId] ?? [];
    return contactMessages[contactMessages.length - 1]?.content ?? "";
  }

  return (
    <div className="flex h-[75vh] overflow-hidden rounded-lg border border-gray-200 bg-white">
      <div
        className={`w-full border-r border-gray-200 lg:block lg:w-80 ${
          selectedContactId ? "hidden" : "block"
        }`}
      >
        <ContactsSidebar
          selectedContactId={selectedContactId}
          onSelectContact={setSelectedContactId}
          lastMessagePreview={lastMessagePreview}
        />
      </div>

      <div className={`min-w-0 flex-1 lg:block ${selectedContactId ? "block" : "hidden"}`}>
        {selectedContact ? (
          <ConversationView
            contact={selectedContact}
            messages={messagesByContact[selectedContact.id] ?? []}
            onSendMessage={handleSend}
            onBackToList={() => setSelectedContactId(null)}
          />
        ) : (
          <div className="hidden h-full items-center justify-center text-sm text-gray-400 lg:flex">
            Selecione uma conversa para começar
          </div>
        )}
      </div>
    </div>
  );
}

