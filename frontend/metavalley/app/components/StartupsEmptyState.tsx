import { Rocket } from "lucide-react";

export default function StartupsEmptyState() {
  return (
    <div className="flex h-56 w-full flex-col items-center justify-center gap-3 rounded-md border border-dashed border-gray-300 bg-gray-50 text-gray-400">
      <Rocket size={32} className="text-gray-300" />
      <p className="text-sm">Suas startups apareceram aqui. Experimente criar uma.</p>
    </div>
  );
}

