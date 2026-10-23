import { NavLink } from "react-router-dom";
import { Home, Database, AudioLines, MessageSquare, Link2, BarChart2, FileText, Settings } from "lucide-react";
import { cn } from "../../lib/cn";

const tabs = [
  { to: "/", label: "Overview", icon: Home, end: true },
  { to: "/data-quality", label: "Data Quality", icon: Database },
  { to: "/asr-analysis", label: "ASR Analysis", icon: AudioLines },
  { to: "/llm-review", label: "LLM Review", icon: MessageSquare },
  { to: "/end-to-end", label: "End-to-End", icon: Link2 },
  { to: "/regression", label: "Regression", icon: BarChart2 },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/configuration", label: "Configuration", icon: Settings },
];

export function TopNav() {
  return (
    <header className="bg-[#0f1535] text-white">
      <div className="flex items-center justify-between px-5 py-3">
        <div className="flex items-center gap-2 font-semibold">
          <AudioLines size={20} className="text-indigo-400" />
          Speech & LLM Quality Lab
          <span className="ml-2 rounded-full bg-indigo-500/20 px-2 py-0.5 text-xs text-indigo-300">
            Beta design preview
          </span>
        </div>
        <div className="text-sm text-slate-300">Local workspace ▾</div>
      </div>
      <nav className="flex gap-1 px-3 pb-2">
        {tabs.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm",
                isActive ? "bg-indigo-600 text-white" : "text-slate-300 hover:bg-white/10"
              )
            }
          >
            <Icon size={15} />
            {label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}