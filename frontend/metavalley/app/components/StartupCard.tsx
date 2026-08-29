import { Rocket } from "lucide-react";
import type Startup from "@/features/startups/startup.types";

interface StartupCardProps {
  startup: Startup;
}

export default function StartupCard({ startup }: StartupCardProps) {
  return (
    <div className="cursor-pointer w-full max-w-[220px] overflow-hidden rounded-md border border-gray-200 bg-white">
      <div className="flex h-32 w-full items-center justify-center bg-gray-100">
        {/* TODO: trocar por <Image> com a foto da startup quando o upload estiver disponível */}
        <Rocket className="text-gray-400" size={32} />
      </div>
      <p className="border-t border-gray-100 p-3 text-sm font-medium text-gray-900">
        {startup.name}
      </p>
    </div>
  );
}

