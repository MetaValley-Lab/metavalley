"use client";

import { useState } from "react";
import type { ChatContact, ChatMessage } from "@/features/startups/chat/chat.types";
import { getContactById } from "@/features/startups/chat/chat-data";
import ChatHeader from "@/app/components/ChatHeader";
import ContactDetailPanel from "@/app/components/ContactDetailPanel";
import MessageBubble from "@/app/components/MessageBubble";
import MessageInput from "@/app/components/MessageInput";
import TypingIndicator from "./TypingIndicator";

interface ConversationViewProps {
  contact: ChatContact;
  messages: ChatMessage[];
  onSendMessage: (content: string) => void;
  onBackToList: () => void;
  typingAgents: string[];
}

export default function ConversationView({
  contact,
  messages,
  onSendMessage,
  onBackToList,
  typingAgents = []
}: ConversationViewProps) {
  const [showDetails, setShowDetails] = useState(false);

  if (showDetails) {
    return <ContactDetailPanel contact={contact} onBack={() => setShowDetails(false)} />;
  }

  return (
    <div className="flex h-full flex-col">
      <ChatHeader contact={contact} onOpenDetails={() => setShowDetails(true)} onBack={onBackToList} />

      <div className="flex-1 space-y-3 overflow-y-auto bg-gray-50 p-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} showAgentIdentity={contact.isGroup} />
        ))}

        {typingAgents.map((agentId) => {
          const typingContact = getContactById(agentId) ?? contact;
          return <TypingIndicator key={agentId} contact={typingContact} />;
        })}
        
      </div>

      <MessageInput onSend={onSendMessage} />
    </div>
  );
}