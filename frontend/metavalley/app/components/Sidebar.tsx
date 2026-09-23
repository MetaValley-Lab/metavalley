"use client";

import { useEffect, useState, type ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  PanelLeftClose,
  PanelLeftOpen,
  Search,
  LayoutDashboard,
  BarChart3,
  Globe,
  Lightbulb,
  FlaskConical,
  Pencil,
  type LucideIcon,
} from "lucide-react";
import Modal from "./Modal";
import EditProfileModal from "./EditProfileModal";
import { getProfile } from "@/features/auth/profile.service";
import type { UserProfile } from "@/features/auth/profile.types";

interface StubFeature {
  id: string;
  label: string;
  icon: LucideIcon;
  title: string;
  description: string;
}

const relatoriosStub: StubFeature = {
  id: "relatorios",
  label: "Relatórios",
  icon: BarChart3,
  title: "Relatórios",
  description: "Relatórios detalhados sobre o andamento das suas startups.",
};

const analyticsStubs: StubFeature[] = [
  {
    id: "analytics-overview",
    label: "Overview",
    icon: Globe,
    title: "Overview",
    description: "Um panorama geral de como a sua ideia está posicionada no mundo...",
  },
  {
    id: "analytics-insights",
    label: "Insights",
    icon: Lightbulb,
    title: "Insights",
    description: "Direcionamentos e dicas de como seguir com a sua ideia...",
  },
  {
    id: "analytics-experimento",
    label: "Experimento",
    icon: FlaskConical,
    title: "Experimento",
    description: "Crie um experimento para que pessoas reais tenham uma prévia...",
  },
];

interface NavLinkItemProps {
  href: string;
  icon: LucideIcon;
  label: string;
  expanded: boolean;
  active: boolean;
}

function NavLinkItem({ href, icon: Icon, label, expanded, active }: NavLinkItemProps) {
  return (
    <Link
      href={href}
      className={`flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
        active ? "bg-white font-semibold text-gray-900 shadow-sm" : "text-gray-500 hover:bg-gray-200"
      } ${!expanded ? "justify-center" : ""}`}
    >
      <Icon size={18} className="shrink-0" />
      {expanded && <span className="truncate">{label}</span>}
    </Link>
  );
}

interface NavButtonItemProps {
  icon: LucideIcon;
  label: string;
  expanded: boolean;
  onClick: () => void;
}

function NavButtonItem({ icon: Icon, label, expanded, onClick }: NavButtonItemProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex w-full cursor-pointer items-center gap-3 rounded-lg px-3 py-2 text-left text-sm text-gray-500 transition-colors hover:bg-gray-200 ${
        !expanded ? "justify-center" : ""
      }`}
    >
      <Icon size={18} className="shrink-0" />
      {expanded && <span className="truncate">{label}</span>}
    </button>
  );
}

function SectionLabel({ children, expanded }: { children: ReactNode; expanded: boolean }) {
  if (!expanded) return <div className="my-2 border-t border-gray-200" />;
  return (
    <p className="mb-1 mt-4 px-3 text-xs font-semibold uppercase tracking-wide text-gray-400">
      {children}
    </p>
  );
}

export default function Sidebar() {
  const [expanded, setExpanded] = useState(true);
  const [activeStub, setActiveStub] = useState<StubFeature | null>(null);
  const pathname = usePathname();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [profileModalOpen, setProfileModalOpen] = useState(false);

  useEffect(() => {
    getProfile().then(setProfile).catch(() => setProfile(null));
  }, []);

  return (
    <>
      {/* 1. Alterado: adicionado 'sticky top-0 z-40' para fixar a sidebar na tela durante o scroll */}
      <aside
        className={`sticky top-0 z-40 flex h-screen shrink-0 flex-col border-r border-gray-200 bg-gray-50 py-4 transition-all ${
          expanded ? "w-64" : "w-16"
        }`}
      >
        {/* 2. Alterado: flex-col quando fechado e items-center para alinhar verticalmente */}
        <div className={`flex items-center px-3 ${expanded ? "justify-between" : "flex-col gap-3 justify-center"}`}>
          <Link href="/home" className="flex min-w-0 cursor-pointer items-center gap-2">
            {/* TODO: Trocar para a logo-marga do MetaValley quando existir. */}
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-[#4735FD] text-sm font-bold text-white">
              M
            </span>
            {expanded && <span className="truncate font-bold text-gray-900">MetaValley</span>}
          </Link>
          
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            aria-label={expanded ? "Recolher menu" : "Expandir menu"}
            className="cursor-pointer shrink-0 rounded-full p-1 text-gray-400 hover:bg-gray-200"
          >
            {expanded ? <PanelLeftClose size={16} /> : <PanelLeftOpen size={16} />}
          </button>
        </div>

        <div className="mt-4 px-3">
          <div
            className={`flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-400 ${
              expanded ? "" : "justify-center"
            }`}
          >
            <Search size={16} className="shrink-0" />
            {expanded && <span>Busca rápida</span>}
          </div>
        </div>

        <nav className="mt-4 flex flex-1 flex-col gap-1 overflow-y-auto px-3">
          <NavLinkItem href="/home" icon={LayoutDashboard} label="Dashboard" expanded={expanded} active={pathname === "/home"} />
          <NavButtonItem icon={relatoriosStub.icon} label={relatoriosStub.label} expanded={expanded} onClick={() => setActiveStub(relatoriosStub)} />
          
          <SectionLabel expanded={expanded}>Analytics</SectionLabel>
          
          {analyticsStubs.map((stub) => (
            <NavButtonItem key={stub.id} icon={stub.icon} label={stub.label} expanded={expanded} onClick={() => setActiveStub(stub)} />
          ))}
        </nav>

        {/* 3. Alterado: centraliza a foto do usuário quando a sidebar está recolhida */}
        <div className="border-t border-gray-200 px-3 pt-3">
          <div className={`flex items-center gap-2 ${!expanded ? "justify-center" : ""}`}>
            {profile?.avatar_url ? <img src={profile.avatar_url} alt="Foto de perfil" className="h-8 w-8 shrink-0 rounded-full object-cover" /> : <div className="h-8 w-8 shrink-0 rounded-full bg-gray-300" />}
            {expanded && (
              <>
                <span className="min-w-0 flex-1 truncate text-sm text-gray-600">{profile?.username ?? "Minha conta"}</span>
                <button type="button" aria-label="Editar perfil" onClick={() => setProfileModalOpen(true)} className="cursor-pointer rounded p-1 text-gray-400 hover:bg-gray-200 hover:text-gray-700"><Pencil size={15} /></button>
              </>
            )}
          </div>
        </div>
      </aside>

      <Modal visible={activeStub !== null} onHide={() => setActiveStub(null)} title={activeStub?.title ?? ""}>
        <p className="mb-1 inline-block rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-700">
          Em desenvolvimento
        </p>
        <p className="mt-3 text-sm text-gray-600">{activeStub?.description}</p>
      </Modal>
      <EditProfileModal
        visible={profileModalOpen}
        profile={profile}
        onHide={() => setProfileModalOpen(false)}
        onSaved={(updatedProfile) => setProfile((current) => ({ ...current, ...updatedProfile }))}
      />
    </>
  );
}
