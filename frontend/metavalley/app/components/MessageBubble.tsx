import type { ChatMessage } from "@/features/startups/chat/chat.types";


interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-2 text-sm ${
          isUser ? "rounded-br-sm bg-[#4735FD] text-white" : "rounded-bl-sm bg-gray-100 text-gray-900"
        }`}
      >
        <p>{message.content}</p>
        <p className={`mt-1 text-[10px] ${isUser ? "text-white/70" : "text-gray-400"}`}>
          {message.timestamp}
        </p>
      </div>
    </div>
  );
}

