"use client";

import { useEffect, useState, useRef } from "react";
import { chatContacts } from "@/features/startups/chat/chat-data";
import type { ChatMessage } from "@/features/startups/chat/chat.types";
import ContactsSidebar from "@/app/components/ContactsSidebar";
import ConversationView from "@/app/components/ConversationView";
import { getChatHistory, sendMessageStream, type StreamEvent } from "@/features/startups/chat/chat.service";

interface ChatLayoutProps {
  startupId: string;
}

export default function ChatLayout({ startupId }: ChatLayoutProps) {
  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);
  const [messagesByContact, setMessagesByContact] = useState<Record<string, ChatMessage[]>>({});
  const [typingAgents, setTypingAgents] = useState<string[]>([]); 
  const [typingResetKey, setTypingResetKey] = useState<string | null>(null);
  
  // Usamos um Ref para memorizar quais conversas já buscaram o histórico na API
  const loadedHistories = useRef<Set<string>>(new Set());

  const selectedContact = chatContacts.find((c) => c.id === selectedContactId) ?? null;


  if (typingResetKey  !== selectedContactId) {
    setTypingResetKey(selectedContactId);
    if (typingAgents.length > 0) setTypingAgents([]);
  }
  

  // 1. CARREGA HISTÓRICO
  useEffect(() => {
    if (!selectedContactId || !startupId || startupId === "undefined") return;
    
    // Checamos o Ref em vez do state. Isso elimina o aviso do ESLint e evita o loop infinito.
    if (loadedHistories.current.has(selectedContactId)) return;

    async function fetchHistory() {
      try {
        const historyData = await getChatHistory(startupId, selectedContactId!);
        
        const formattedMessages: ChatMessage[] = historyData.map((msg) => ({
          id: msg.id,
          contactId: selectedContactId!,
          sender: msg.role === "user" ? "user" : "agent",
          agentName: msg.agent_name,
          content: msg.content,
          timestamp: new Date(msg.created_at).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })
        }));

        setMessagesByContact((prev) => ({
          ...prev,
          [selectedContactId!]: formattedMessages
        }));

        // Marca que esta conversa já foi carregada
        loadedHistories.current.add(selectedContactId!);
      } catch (error) {
        console.error("Erro ao carregar histórico:", error);
      }
    }

    fetchHistory();
    
  }, [selectedContactId, startupId]); 

  // 2. ENVIA MENSAGEM
  async function handleSend(content: string) {
    if (!selectedContactId) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      contactId: selectedContactId,
      sender: "user",
      content,
      timestamp: new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
    };

    setMessagesByContact((prev) => ({
      ...prev,
      [selectedContactId]: [...(prev[selectedContactId] ?? []), userMessage],
    }));

    setTypingAgents([]);

    await sendMessageStream(
      {
        startupId,
        message: content,
        conversationType: selectedContactId,
      },
      (event: StreamEvent) => {
        if (event.event === "agent_start") {
          setTypingAgents((prev) => (prev.includes(event.agent) ? prev : [...prev, event.agent]));
        } else if (event.event === "agent_message") {
          
          setTypingAgents((prev) => prev.filter((agentId) => agentId !== event.agent));

          const agentMessage: ChatMessage = {
            id: `agent-${Date.now()}-${Math.random()}`,
            contactId: selectedContactId,
            sender: "agent",
            agentName: event.agent,
            content: event.content,
            timestamp: new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
          };

          setMessagesByContact((prev) => ({
            ...prev,
            [selectedContactId]: [...(prev[selectedContactId] ?? []), agentMessage],
          }));
        } else if (event.event === "turn_complete") {
          setTypingAgents([]);
        }
      },
      (errorMessage: string) => {
        console.error("Erro do agente:", errorMessage);
        setTypingAgents([]);
      },
      () => {
        setTypingAgents([]);
      }
    );
  }

  function lastMessagePreview(contactId: string): string {
    const contactMessages = messagesByContact[contactId] ?? [];
    return contactMessages[contactMessages.length - 1]?.content ?? "Nenhuma mensagem...";
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
            typingAgents={typingAgents}
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

