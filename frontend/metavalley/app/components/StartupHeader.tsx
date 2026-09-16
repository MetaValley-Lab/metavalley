import { Rocket } from "lucide-react";
import type Startup from "@/features/startups/startup.types";

interface StartupHeaderProps {
  startup: Startup;
}

export default function StartupHeader({ startup }: StartupHeaderProps) {
  return (
    <div className="mb-8">
      <div className="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-gray-200">
        {startup.image_url ? (
          <img src={startup.image_url} alt={`Imagem da startup ${startup.name}`} className="h-full w-full rounded-full object-cover" />
        ) : (
          <Rocket className="text-gray-400" size={32} />
        )}
      </div>
      <h1 className="text-2xl font-bold text-gray-900">{startup.name}</h1>
      {startup.description && (
        <p className="mt-1 text-sm text-gray-600">{startup.description}</p>
      )}
    </div>
  );
}

