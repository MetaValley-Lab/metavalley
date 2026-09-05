"use client";

import { chatContacts } from "@/features/startups/chat/chat-data";
import ContactAvatar from "./ContactAvatar";

interface ContactsSidebarProps {
  selectedContactId: string | null;
  onSelectContact: (contactId: string) => void;
  lastMessagePreview: (contactId: string) => string;
}

export default function ContactsSidebar({
  selectedContactId,
  onSelectContact,
  lastMessagePreview,
}: ContactsSidebarProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-900">Conversas</h2>
      </div>

      <div className="flex-1 overflow-y-auto">
        {chatContacts.map((contact) => (
          <button
            key={contact.id}
            type="button"
            onClick={() => onSelectContact(contact.id)}
            className={`flex w-full cursor-pointer items-center gap-3 border-b border-gray-100 p-3 text-left transition-colors hover:bg-gray-50 ${
              selectedContactId === contact.id ? "bg-gray-100" : ""
            }`}
          >
            <ContactAvatar contact={contact} />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-gray-900">{contact.name}</p>
              <p className="truncate text-xs text-gray-500">{lastMessagePreview(contact.id)}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

