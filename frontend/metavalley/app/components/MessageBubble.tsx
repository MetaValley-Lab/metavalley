import type { ChatMessage } from "@/features/startups/chat/chat.types";
import { getContactById } from "@/features/startups/chat/chat-data";
import ContactAvatar from "./ContactAvatar";

interface MessageBubbleProps {
  message: ChatMessage;
  showAgentIdentity?: boolean;
}

export default function MessageBubble({
  message,
  showAgentIdentity = false,
}: MessageBubbleProps) {
  const isUser = message.sender === "user";
  const agentContact = message.agentName
    ? getContactById(message.agentName)
    : undefined;
  const showIdentity = showAgentIdentity && !isUser && message.agentName;

  return (
    <div
      className={`flex items-end gap-2 ${isUser ? "justify-end" : "justify-start"}`}
    >
      {showIdentity && (
        <div className="self-start">
          {agentContact ? (
            <ContactAvatar contact={agentContact} />
          ) : (
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-gray-300 text-xs font-semibold text-white">
              {message.agentName?.slice(0, 2).toUpperCase()}
            </div>
          )}
        </div>
      )}

      <div className="flex max-w-[75%] flex-col">
        {showIdentity && (
          <p className="mb-0.5 px-1 text-xs font-semibold text-gray-500">
            {agentContact?.name ?? message.agentName}
          </p>
        )}
        <div
          className={`rounded-2xl px-4 py-2 text-sm ${
            isUser
              ? "rounded-br-sm bg-[#4735FD] text-white"
              : "rounded-bl-sm bg-gray-100 text-gray-900"
          }`}
        >
          <p>{message.content}</p>
          <p
            className={`mt-1 text-[10px] ${isUser ? "text-white/70" : "text-gray-400"}`}
          >
            {message.timestamp}
          </p>
        </div>
      </div>
    </div>
  );
}
