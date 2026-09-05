"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";
import { deleteStartup, getStartups } from "@/features/startups/startup.service";
import type Startup  from "@/features/startups/startup.types";
import { ApiError } from "@/lib/api/api-client";
import StartupCard from "./StartupCard";
import StartupsEmptyState from "./StartupsEmptyState";
import CreateStartupModal from "./CreateStartupModal";
import ConfirmModal from "./ConfirmModal";

export default function StartupsGrid() {
  const router = useRouter();
  const [startups, setStartups] = useState<Startup[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingStartup, setEditingStartup] = useState<Startup | null>(null);
  const [deletingStartup, setDeletingStartup] = useState<Startup | null>(null);
  const [deleting, setDeleting] = useState(false);

  async function loadStartups() {
    setLoading(true);
    setError(null);
    try {
      const data = await getStartups();
      setStartups(data);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        router.push("/auth/login");
        return;
      }
      setError("Não foi possível carregar suas startups agora.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    // Busca inicial ao montar o componente. O eslint-plugin-react-hooks
    // recente sinaliza qualquer setState disparado a partir de um efeito
    // (react-hooks/set-state-in-effect), mesmo em fetch-on-mount, um padrão
    // seguro e comum. A alternativa "correta" seria uma lib de data-fetching
    // (SWR/React Query) — decisão maior que não tomei aqui sozinho.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadStartups();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Suas Startups</h2>
        <button
          type="button"
          onClick={() => setModalOpen(true)}
          className="cursor-pointer flex items-center gap-1.5 rounded-full bg-[#4735FD] px-4 py-2 text-sm font-semibold text-white hover:bg-[#3c2ce0]"
        >
          <Plus size={16} />
          Criar nova startup
        </button>
      </div>

      {loading ? (
        <div className="h-56 w-full animate-pulse rounded-md bg-gray-100" />
      ) : error ? (
        <div className="flex h-56 w-full items-center justify-center rounded-md border border-gray-200 text-sm text-gray-500">
          {error}
        </div>
      ) : startups.length === 0 ? (
        <StartupsEmptyState />
      ) : (
        <div className="flex flex-wrap gap-4">
          {startups.map((startup) => (
            <StartupCard
              key={startup.id}
              startup={startup}
              onEdit={(item) => { setEditingStartup(item); setModalOpen(true); }}
              onDelete={setDeletingStartup}
            />
          ))}
        </div>
      )}

      <CreateStartupModal
        visible={modalOpen}
        startup={editingStartup}
        onHide={() => { setModalOpen(false); setEditingStartup(null); }}
        onCreated={() => {
          setModalOpen(false);
          setEditingStartup(null);
          loadStartups();
        }}
      />
      <ConfirmModal
        visible={Boolean(deletingStartup)}
        title="Excluir startup"
        message={`Tem certeza que deseja excluir a startup "${deletingStartup?.name ?? ""}"?`}
        isSubmitting={deleting}
        onHide={() => setDeletingStartup(null)}
        onConfirm={async () => {
          if (!deletingStartup) return;
          setDeleting(true);
          try {
            await deleteStartup(deletingStartup.id);
            setDeletingStartup(null);
            await loadStartups();
          } finally {
            setDeleting(false);
          }
        }}
      />
    </section>
  );
}

