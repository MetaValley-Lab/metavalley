interface ComingSoonProps {
  title: string;
}

export default function ComingSoon({ title }: ComingSoonProps) {
  return (
    <div className="flex h-56 w-full flex-col items-center justify-center gap-2 rounded-md border border-dashed border-gray-300 bg-gray-50 text-center text-gray-400">
      <p className="text-sm font-medium">{title}</p>
      <p className="text-xs">Essa área ainda está em construção.</p>
    </div>
  );
}

