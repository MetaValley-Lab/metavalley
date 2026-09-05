"use client";

import { useEffect, useState, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import { getStartup } from "@/features/startups/startup.service";
import type Startup from "@/features/startups/startup.types";
import { ApiError } from "@/lib/api/api-client";
import StartupHeader from "./StartupHeader";
import WorkspaceTabs from "./WorkspaceTabs";


interface StartupWorkspaceShellProps {
  startupId: string;
  children: ReactNode;
}

export default function StartupWorkspaceShell({ startupId, children }: StartupWorkspaceShellProps) {
  const router = useRouter();
  const [startup, setStartup] = useState<Startup | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStartup() {
      setLoading(true);
      setError(null);
      try {
        const data = await getStartup(startupId);
        setStartup(data);
      } catch (err) {
        if (err instanceof ApiError && err.status === 401) {
          router.push("/auth/login");
          return;
        }
        setError("Não foi possível carregar essa startup agora.");
      } finally {
        setLoading(false);
      }
    }
    loadStartup();
  }, [startupId, router]);

  return (
    <div className="mx-auto max-w-5xl p-8">
      <WorkspaceTabs startupId={startupId} />

      <div className="mt-6">
        {loading ? (
          <div className="mb-8 flex items-center gap-4">
            <div className="h-20 w-20 animate-pulse rounded-full bg-gray-200" />
            <div className="flex flex-col gap-2">
              <div className="h-6 w-40 animate-pulse rounded bg-gray-200" />
              <div className="h-4 w-64 animate-pulse rounded bg-gray-100" />
            </div>
          </div>
        ) : error ? (
          <p className="mb-8 text-sm text-red-500">{error}</p>
        ) : startup ? (
          <StartupHeader startup={startup} />
        ) : null}

        {children}
      </div>
    </div>
  );
}

