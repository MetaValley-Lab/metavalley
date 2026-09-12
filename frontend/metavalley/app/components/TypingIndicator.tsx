import type { ChatContact } from "@/features/startups/chat/chat.types";
import ContactAvatar from "./ContactAvatar";

interface TypingIndicatorProps {
  contact: ChatContact;
}

export default function TypingIndicator({ contact }: TypingIndicatorProps) {
  return (
    <div className="flex items-end gap-2">
      <ContactAvatar contact={contact} />
      <div className="flex items-center gap-1 rounded-2xl rounded-bl-sm bg-gray-100 px-4 py-3">
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-gray-400 [animation-delay:-0.3s]" />
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-gray-400 [animation-delay:-0.15s]" />
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-gray-400" />
      </div>
    </div>
  );
}

