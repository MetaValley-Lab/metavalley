import { canvasZoneTitles, canvasZoneEmptyText, filledByLabels } from "@/features/startups/canvas/canvas-zone";
import { CanvasZone } from "@/features/startups/canvas/canvas.types";


const statusBorderClass: Record<string, string> = {
  filled: "border-l-4 border-l-green-500",
  in_progress: "border-l-4 border-l-amber-400",
  to_define: "border-l-4 border-l-transparent",
};

interface CanvasZoneCardProps {
  zone: CanvasZone;
}

export default function CanvasZoneCard({ zone }: CanvasZoneCardProps) {
  const title = canvasZoneTitles[zone.zone_key] ?? zone.zone_key;
  const borderClass = statusBorderClass[zone.status] ?? statusBorderClass.to_define;
  const filledByLabel = filledByLabels[zone.filled_by] ?? zone.filled_by;
  const emptyText = canvasZoneEmptyText[zone.zone_key] ?? "Ainda não definido.";

  return (
    <div className={`rounded-md border border-gray-200 bg-white p-4 ${borderClass}`}>
      <div className="mb-1 flex items-start justify-between gap-2">
        <h3 className="text-sm font-bold uppercase tracking-wide text-gray-900">{title}</h3>
        {zone.filled_by && (
          <span className="shrink-0 rounded-full border border-gray-200 px-2 py-0.5 text-[10px] font-semibold text-gray-500">
            {filledByLabel}
          </span>
        )}
      </div>
      <p className="text-sm text-gray-600">{zone.content || emptyText}</p>
    </div>
  );
}

