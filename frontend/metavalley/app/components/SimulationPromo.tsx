// Local: features/simulation/components/SimulationPromo.tsx

"use client";

import { useEffect, useState } from "react";
import { Orbit, Lock, Check } from "lucide-react";
import {
  getMySimulationInterest,
  createSimulationInterest,
  deleteSimulationInterest,
} from "@/features/startups/simulation/simulation.service";

import Button from "@/app/components/Button";

interface SimulationPromoProps {
  startupId: string;
}

// TODO: ainda sem destino definido. Quando a página/seção de detalhes da
// Simulação (TME) existir, troque o conteúdo desta função por uma navegação
// (ex: router.push("/algum-lugar")) ou pela abertura de um modal.
function handleLearnMore() {
  // Propositalmente vazio por enquanto.
}

export default function SimulationPromo({ startupId }: SimulationPromoProps) {
  const [interested, setInterested] = useState(false);
  const [interestId, setInterestId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStatus() {
      setLoading(true);
      try {
        const status = await getMySimulationInterest(startupId);
        setInterested(status.interested);
      } catch {
        // Se a checagem falhar, deixa o usuário tentar se inscrever normalmente
        // em vez de travar a tela com um erro.
      } finally {
        setLoading(false);
      }
    }
    loadStatus();
  }, [startupId]);

  async function handleSubscribe() {
    setSubmitting(true);
    setError(null);
    try {
      const created = await createSimulationInterest(startupId);
      setInterestId(created.id);
      setInterested(true);
    } catch {
      setError("Não foi possível confirmar sua inscrição agora. Tente novamente.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleUnsubscribe() {
    if (!interestId) return;
    setSubmitting(true);
    setError(null);
    try {
      await deleteSimulationInterest(interestId);
      setInterestId(null);
      setInterested(false);
    } catch {
      setError("Não foi possível cancelar a inscrição agora.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="mx-auto flex max-w-xl flex-col items-center gap-4 rounded-lg border border-gray-200 bg-white px-8 py-12 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[#4735FD]/10 text-[#4735FD]">
        <Orbit size={32} />
      </div>

      <span className="flex items-center gap-1 rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-500">
        <Lock size={12} />
        Recurso Premium
      </span>

      <h2 className="text-2xl font-bold text-gray-900">Simulação de Mercado (TME)</h2>

      <p className="max-w-md text-sm text-gray-600">
        Valide suas ideias e produtos num mercado sintético antes de gastar tempo e dinheiro
        construindo de verdade. A Simulação ainda está em desenvolvimento — inscreva-se para ser
        avisado assim que ela estiver disponível.
      </p>

      {loading ? (
        <div className="h-11 w-48 animate-pulse rounded-md bg-gray-100" />
      ) : interested ? (
        <div className="flex flex-col items-center gap-2">
          <p className="flex items-center gap-2 text-sm font-semibold text-green-600">
            <Check size={16} />
            Você está na lista de espera
          </p>
          {interestId && (
            <button
              type="button"
              onClick={handleUnsubscribe}
              disabled={submitting}
              className="cursor-pointer text-xs text-gray-400 underline hover:text-gray-600 disabled:cursor-not-allowed"
            >
              Cancelar inscrição
            </button>
          )}
        </div>
      ) : (
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button
            label={submitting ? "Enviando..." : "Quero ser notificado"}
            type="button"
            onClick={handleSubscribe}
            disabled={submitting}
            className="w-auto px-6"
          />
          <button
            type="button"
            onClick={handleLearnMore}
            className="cursor-pointer rounded-md border border-gray-300 px-6 py-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-50"
          >
            Saiba mais
          </button>
        </div>
      )}

      {error && <p className="text-xs text-red-500">{error}</p>}
    </section>
  );
}

