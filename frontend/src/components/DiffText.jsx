import { diffWords } from "diff";
import { cn } from "../lib/cn";

export function DiffText({ reference, prediction }) {
  const parts = diffWords(reference, prediction);

  return (
    <div className="flex flex-wrap gap-1">
      {parts.map((part, i) => (
        <span
          key={i}
          className={cn(
            "rounded px-1.5 py-0.5 text-sm",
            part.added && "bg-red-100 text-red-700",
            part.removed && "bg-amber-100 text-amber-700 line-through",
            !part.added && !part.removed && "text-slate-700"
          )}
        >
          {part.value}
        </span>
      ))}
    </div>
  );
}