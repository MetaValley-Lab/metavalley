import { Users, Briefcase, Code2, Wallet, Megaphone, type LucideIcon } from "lucide-react";
import type { ChatContact } from "@/features/startups/chat/chat.types";

const roleIcons: Record<string, LucideIcon> = {
  ceo: Briefcase,
  cto: Code2,
  cfo: Wallet,
  cmo: Megaphone,
};

interface ContactAvatarProps {
  contact: ChatContact;
  size?: "sm" | "lg";
}

export default function ContactAvatar({ contact, size = "sm" }: ContactAvatarProps) {
  const Icon = contact.isGroup ? Users : (roleIcons[contact.id] ?? Users);
  const dimensionClass = size === "lg" ? "h-20 w-20" : "h-11 w-11";
  const iconSize = size === "lg" ? 32 : 20;

  return (
    <div
      className={`flex ${dimensionClass} shrink-0 items-center justify-center rounded-full text-white ${contact.color}`}
    >
      {/* TODO: trocar pela foto real do contato quando existir */}
      <Icon size={iconSize} />
    </div>
  );
}

