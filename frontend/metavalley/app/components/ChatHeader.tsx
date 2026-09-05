// Local: features/chat/components/ChatHeader.tsx

import { ChevronLeft } from "lucide-react";
import type { ChatContact } from "@/features/startups/chat/chat.types";
import ContactAvatar from "@/app/components/ContactAvatar";

interface ChatHeaderProps {
  contact: ChatContact;
  onOpenDetails: () => void;
  onBack: () => void;
}

export default function ChatHeader({ contact, onOpenDetails, onBack }: ChatHeaderProps) {
  return (
    <div className="flex items-center gap-1 border-b border-gray-200 p-2">
      <button
        type="button"
        onClick={onBack}
        aria-label="Voltar para a lista de conversas"
        className="cursor-pointer rounded-full p-2 text-gray-500 hover:bg-gray-100 lg:hidden"
      >
        <ChevronLeft size={20} />
      </button>

      <button
        type="button"
        onClick={onOpenDetails}
        className="flex flex-1 cursor-pointer items-center gap-3 rounded-md p-1 text-left hover:bg-gray-50"
      >
        <ContactAvatar contact={contact} />
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-gray-900">{contact.name}</p>
          <p className="truncate text-xs text-gray-400">Toque para ver os detalhes do contato</p>
        </div>
      </button>
    </div>
  );
}

