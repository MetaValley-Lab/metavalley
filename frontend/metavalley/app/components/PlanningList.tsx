"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ListTodo } from "lucide-react";
import {
  getPlanningItems,
  createPlanningItem,
  updatePlanningItem,
  deletePlanningItem,
} from "@/features/startups/planning/planning.service";
import type { PlanningItem } from "@/features/startups/planning/planning.types";
import { ApiError } from "@/lib/api/api-client";
import PlanningItemRow from "./PlanningItemRow";
import CreatePlanningItemForm from "./CreatePlanningItemForm";

interface PlanningListProps {
  startupId: string;
}

export default function PlanningList({ startupId }: PlanningListProps) {
  const router = useRouter();
  const [items, setItems] = useState<PlanningItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    async function loadItems() {
      setLoading(true);
      setLoadError(null);
      try {
        const data = await getPlanningItems(startupId);
        setItems(data);
      } catch (err) {
        if (err instanceof ApiError && err.status === 401) {
          router.push("/auth/login");
          return;
        }
        setLoadError("Não foi possível carregar as tarefas agora.");
      } finally {
        setLoading(false);
      }
    }
    loadItems();
  }, [startupId, router]);

  async function handleCreate(content: string) {
    setCreating(true);
    setActionError(null);
    try {
      const newItem = await createPlanningItem({ startup_id: startupId, content });
      setItems((prev) => [newItem, ...prev]);
    } catch {
      setActionError("Não foi possível criar a tarefa agora.");
    } finally {
      setCreating(false);
    }
  }

  async function handleToggleComplete(item: PlanningItem) {
    setActionError(null);
    const previousItems = items;
    // Atualização otimista: reflete a mudança na tela antes da resposta do backend,
    // e desfaz se a chamada falhar.
    setItems((prev) => prev.map((i) => (i.id === item.id ? { ...i, completed: !i.completed } : i)));
    try {
      const updated = await updatePlanningItem(item.id, { completed: !item.completed });
      setItems((prev) => prev.map((i) => (i.id === item.id ? updated : i)));
    } catch {
      setItems(previousItems);
      setActionError("Não foi possível atualizar a tarefa agora.");
    }
  }

  async function handleDelete(item: PlanningItem) {
    setActionError(null);
    const previousItems = items;
    setItems((prev) => prev.filter((i) => i.id !== item.id));
    try {
      await deletePlanningItem(item.id);
    } catch {
      setItems(previousItems);
      setActionError("Não foi possível excluir a tarefa agora.");
    }
  }

  return (
    <section>
      <h2 className="mb-3 text-lg font-semibold text-gray-900">Lista de Tarefas</h2>

      <div className="rounded-lg border border-gray-200 bg-white">
        <CreatePlanningItemForm onCreate={handleCreate} creating={creating} />

        {actionError && (
          <p className="border-b border-gray-100 bg-red-50 px-3 py-2 text-xs text-red-600">
            {actionError}
          </p>
        )}

        {loading ? (
          <div className="space-y-2 p-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="h-10 animate-pulse rounded-md bg-gray-100" />
            ))}
          </div>
        ) : loadError ? (
          <p className="p-4 text-sm text-red-500">{loadError}</p>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center gap-2 p-10 text-center text-gray-400">
            <ListTodo size={28} className="text-gray-300" />
            <p className="text-sm">Nenhuma tarefa ainda. Adicione a primeira acima.</p>
          </div>
        ) : (
          <div>
            {items.map((item) => (
              <PlanningItemRow
                key={item.id}
                item={item}
                onToggleComplete={handleToggleComplete}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}


