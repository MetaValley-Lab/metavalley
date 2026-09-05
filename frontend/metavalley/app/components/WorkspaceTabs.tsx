"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface WorkspaceTabsProps {
  startupId: string;
}

const tabs = [
  { label: "Painel Principal", href: "" },
  { label: "Chat", href: "/chat" },
  { label: "Lista de Tarefas", href: "/tasks" },
  { label: "Criar produtos", href: "/create-product" },
  { label: "Simulação", href: "/simulation" },
];

export default function WorkspaceTabs({ startupId }: WorkspaceTabsProps) {
  const pathname = usePathname();
  const basePath = `/startups/${startupId}`;

  return (
    <nav className="flex gap-1 overflow-x-auto border-b border-gray-200">
      {tabs.map((tab) => {
        const href = `${basePath}${tab.href}`;
        const isActive = pathname === href;
        return (
          <Link
            key={tab.label}
            href={href}
            className={`cursor-pointer whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium transition-colors ${
              isActive
                ? "border-[#4735FD] text-[#4735FD]"
                : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
            }`}
          >
            {tab.label}
          </Link>
        );
      })}
    </nav>
  );
}

