import { ChevronLeft } from "lucide-react";
import type { ChatContact } from "@/features/startups/chat/chat.types";

import ContactAvatar from "@/app/components/ContactAvatar";

interface ContactDetailPanelProps {
  contact: ChatContact;
  onBack: () => void;
}

export default function ContactDetailPanel({ contact, onBack }: ContactDetailPanelProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-gray-200 p-2">
        <button
          type="button"
          onClick={onBack}
          aria-label="Voltar para a conversa"
          className="cursor-pointer rounded-full p-2 text-gray-500 hover:bg-gray-100"
        >
          <ChevronLeft size={20} />
        </button>
        <p className="text-sm font-semibold text-gray-900">Dados do contato</p>
      </div>

      <div className="flex flex-1 flex-col items-center gap-4 overflow-y-auto p-8 text-center">
        <ContactAvatar contact={contact} size="lg" />
        <h3 className="text-xl font-bold text-gray-900">{contact.name}</h3>
        <p className="max-w-sm text-sm text-gray-600">{contact.description}</p>
      </div>
    </div>
  );
}


