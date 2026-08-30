"use client";

import { useEffect, useState } from "react";
import { getCanvasZones } from "@/features/startups/canvas/canvas.service";
import type { CanvasZone } from "@/features/startups/canvas/canvas.types";
import { canvasZoneOrder } from "@/features/startups/canvas/canvas-zone";

import CanvasZoneCard from "./CanvasZoneCard";

interface CanvasSectionProps {
  startupId: string;
}

function orderIndex(zoneKey: string): number {
  const idx = canvasZoneOrder.indexOf(zoneKey as (typeof canvasZoneOrder)[number]);
  return idx === -1 ? canvasZoneOrder.length : idx;
}

export default function CanvasSection({ startupId }: CanvasSectionProps) {
  const [zones, setZones] = useState<CanvasZone[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadZones() {
      setLoading(true);
      setError(null);
      try {
        const data = await getCanvasZones(startupId);
        setZones([...data].sort((a, b) => orderIndex(a.zone_key) - orderIndex(b.zone_key)));
      } catch {
        setError("Não foi possível carregar o canvas agora.");
      } finally {
        setLoading(false);
      }
    }
    loadZones();
  }, [startupId]);

  return (
    <section className="mb-8">
      <h2 className="mb-3 text-lg font-semibold text-gray-900">Canvas</h2>

      <div className="rounded-lg border border-gray-200 p-4">
        {loading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-24 animate-pulse rounded-md bg-gray-100" />
            ))}
          </div>
        ) : error ? (
          <p className="text-sm text-red-500">{error}</p>
        ) : zones.length === 0 ? (
          <p className="text-sm text-gray-400">Nenhuma zona de canvas encontrada ainda.</p>
        ) : (
          <div className="flex flex-col gap-4">
            {zones[0] && <CanvasZoneCard zone={zones[0]} />}
            {zones.length > 1 && (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                {zones.slice(1).map((zone) => (
                  <CanvasZoneCard key={zone.id} zone={zone} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}

