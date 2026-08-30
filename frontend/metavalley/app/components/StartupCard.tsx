import { Rocket } from "lucide-react";
import type Startup from "@/features/startups/startup.types";
import Link  from "next/link";

interface StartupCardProps {
  startup: Startup;
}

export default function StartupCard({ startup }: StartupCardProps) {
  return (
    <Link 
      href={`/startups/${startup.id}`} 
      className="block cursor-pointer w-full max-w-[220px] overflow-hidden rounded-md border border-gray-200 bg-white transition hover:border-gray-300 hover:shadow-sm"
    >
      <div className="flex h-32 w-full items-center justify-center bg-gray-100">
        {/* TODO: trocar por <Image> com a foto da startup quando o upload estiver disponível */}
        <Rocket className="text-gray-400" size={32} />
      </div>
      <p className="border-t border-gray-100 p-3 text-sm font-medium text-gray-900">
        {startup.name}
      </p>
    </Link>
  );
}

