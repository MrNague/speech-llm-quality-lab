import { BrowserRouter, Routes, Route } from "react-router-dom";
import { TopNav } from "./components/layout/TopNav";
import DataQuality from "./pages/DataQuality";
import AsrAnalysis from "./pages/AsrAnalysis";

export default function App() {
  return (
    <BrowserRouter>
      <TopNav />
      <Routes>
        <Route path="/" element={<div className="p-6"><h1 className="text-xl font-semibold">Overview</h1><p className="text-slate-500">Page in development</p></div>} />
        <Route path="/data-quality" element={<DataQuality />} />
        <Route path="/asr-analysis" element={<AsrAnalysis />} />
        <Route path="/llm-review" element={<div className="p-6"><h1 className="text-xl font-semibold">LLM Review</h1><p className="text-slate-500">Page in development</p></div>} />
        <Route path="/end-to-end" element={<div className="p-6"><h1 className="text-xl font-semibold">End-to-End</h1><p className="text-slate-500">Page in development</p></div>} />
        <Route path="/regression" element={<div className="p-6"><h1 className="text-xl font-semibold">Regression</h1><p className="text-slate-500">Page in development</p></div>} />
        <Route path="/reports" element={<div className="p-6"><h1 className="text-xl font-semibold">Reports</h1><p className="text-slate-500">Page in development</p></div>} />
        <Route path="/configuration" element={<div className="p-6"><h1 className="text-xl font-semibold">Configuration</h1><p className="text-slate-500">Page in development</p></div>} />
      </Routes>
    </BrowserRouter>
  );
}