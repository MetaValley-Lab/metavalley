import { Rocket } from "lucide-react";
import type Startup from "@/features/startups/startup.types";

interface StartupHeaderProps {
  startup: Startup;
}

export default function StartupHeader({ startup }: StartupHeaderProps) {
  return (
    <div className="mb-8">
      <div className="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-gray-200">
        {/* TODO: trocar por <Image> com a foto da startup quando o upload estiver disponível */}
        <Rocket className="text-gray-400" size={32} />
      </div>
      <h1 className="text-2xl font-bold text-gray-900">{startup.name}</h1>
      {startup.description && (
        <p className="mt-1 text-sm text-gray-600">{startup.description}</p>
      )}
    </div>
  );
}

