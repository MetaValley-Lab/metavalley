"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getStartups } from "@/features/startups/startup.service";
import type Startup from "@/features/startups/startup.types";
import { ApiError } from "@/lib/api/api-client";
import Carousel from "./Carousel";

const stageLabels: Record<Startup["stage"], string> = {
  idea: "Ideia",
  mvp: "MVP",
  launched: "Lançada",
};

function InsightField({ label, value }: { label: string; value: string | null }) {
  return (
    <div>
      <p className="text-[10px] font-semibold uppercase tracking-wide text-white/60">{label}</p>
      <p className="mt-0.5 line-clamp-2 text-xs leading-5 text-white/90">
        {value?.trim() || "Ainda não informado"}
      </p>
    </div>
  );
}

export default function StartupInsightsCarousel() {
  const router = useRouter();
  const [startups, setStartups] = useState<Startup[]>([]);

  useEffect(() => {
    getStartups()
      .then(setStartups)
      .catch((error) => {
        if (error instanceof ApiError && error.status === 401) {
          router.push("/auth/login");
        }
      });
  }, [router]);

  const slides = startups.map((startup) => ({
    id: startup.id,
    content: (
      <article className="h-full w-full bg-[#28234f] px-8 py-5 text-white sm:px-12 sm:py-6">
        <div className="flex h-full flex-col justify-between pr-8 sm:pr-10">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#b9b1ff]">
              Insight da startup
            </p>
            <h2 className="mt-1 text-xl font-bold sm:text-2xl">{startup.name}</h2>
            {startup.description && (
              <p className="mt-1 line-clamp-1 text-xs text-white/70">{startup.description}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-x-6 gap-y-3 sm:grid-cols-4">
            <InsightField label="Problema" value={startup.problem} />
            <InsightField label="Solução" value={startup.solution} />
            <InsightField label="Estágio" value={stageLabels[startup.stage]} />
          </div>
        </div>
      </article>
    ),
  }));

  return <Carousel slides={slides} />;
}