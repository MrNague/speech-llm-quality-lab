import { useState } from "react";
import { Card, CardHeader } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { Checkbox } from "../components/ui/Checkbox";
import { reportCase, shareOptions } from "../mocks/reportsData";
import { Share2, X, Download, Link } from "lucide-react";

export default function Reports() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [shareSelection, setShareSelection] = useState({
    transcript: true,
    reference: true,
    audio: false,
    modelConfig: true,
    reviewerNotes: false,
  });
  const [purpose, setPurpose] = useState("internal");
  const [retention, setRetention] = useState("90d");

  const handleShareToggle = (key) => {
    setShareSelection((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleShare = () => {
    console.log("Sharing:", { purpose, retention, ...shareSelection });
    alert("Case shared successfully!");
    setDrawerOpen(false);
  };

  const handleExport = () => {
    console.log("Exporting report...");
    alert("Report downloaded!");
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(`https://lab.example.com/cases/${reportCase.id}`);
    alert("Link copied to clipboard!");
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Reports</h1>
          <p className="text-sm text-slate-500">
            View and share case reports.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={handleCopyLink}>
            <Link size={16} />
            Copy Link
          </Button>
          <Button variant="secondary" onClick={handleExport}>
            <Download size={16} />
            Export
          </Button>
          <Button onClick={() => setDrawerOpen(true)}>
            <Share2 size={16} />
            Share this case
          </Button>
        </div>
      </div>

      {/* Report Preview */}
      <div className="grid grid-cols-2 gap-5">
        {/* Case Info */}
        <Card>
          <CardHeader title="Case Information" />
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-500">Case ID</span>
              <span className="font-medium">{reportCase.caseId}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Report ID</span>
              <span className="font-medium">{reportCase.id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Created</span>
              <span className="font-medium">
                {new Date(reportCase.createdAt).toLocaleDateString("fr-FR")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Status</span>
              <Badge variant="success">{reportCase.status}</Badge>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Audio Duration</span>
              <span className="font-medium">{reportCase.audioDuration}</span>
            </div>
          </div>
        </Card>

        {/* Model Config */}
        <Card>
          <CardHeader title="Model Configuration" />
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-500">Model</span>
              <span className="font-medium">{reportCase.modelConfig.model}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Language</span>
              <span className="font-medium">{reportCase.modelConfig.language}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Temperature</span>
              <span className="font-medium">{reportCase.modelConfig.temperature}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">WER</span>
              <Badge variant={reportCase.wer < 10 ? "success" : "warning"}>
                {reportCase.wer}%
              </Badge>
            </div>
          </div>
        </Card>

        {/* Reference Transcript */}
        <Card>
          <CardHeader title="Reference Transcript" />
          <p className="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg">
            {reportCase.reference}
          </p>
        </Card>

        {/* Model Prediction */}
        <Card>
          <CardHeader title="Model Prediction" />
          <p className="text-sm text-slate-700 bg-indigo-50 p-3 rounded-lg">
            {reportCase.modelPrediction}
          </p>
        </Card>

        {/* Reviewer Notes - Full width */}
        <Card className="col-span-2">
          <CardHeader title="Reviewer Notes" />
          <p className="text-sm text-slate-700 bg-amber-50 p-4 rounded-lg border border-amber-100">
            {reportCase.reviewerNotes}
          </p>
        </Card>
      </div>

      {/* Share Drawer (overlay) */}
      {drawerOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/50 z-40"
            onClick={() => setDrawerOpen(false)}
          />
          
          {/* Drawer */}
          <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-xl z-50 overflow-y-auto">
            <div className="p-5">
              {/* Header */}
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-lg font-semibold">Share this case</h2>
                <button
                  onClick={() => setDrawerOpen(false)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  <X size={20} />
                </button>
              </div>

              {/* Include options */}
              <div className="mb-5">
                <h3 className="text-sm font-medium text-slate-800 mb-3">
                  Include in share
                </h3>
                <div className="space-y-2">
                  <label className="flex items-center gap-3">
                    <Checkbox
                      checked={shareSelection.transcript}
                      onChange={() => handleShareToggle("transcript")}
                    />
                    <span className="text-sm text-slate-700">Transcript</span>
                  </label>
                  <label className="flex items-center gap-3">
                    <Checkbox
                      checked={shareSelection.reference}
                      onChange={() => handleShareToggle("reference")}
                    />
                    <span className="text-sm text-slate-700">Reference</span>
                  </label>
                  <label className="flex items-center gap-3">
                    <Checkbox
                      checked={shareSelection.audio}
                      onChange={() => handleShareToggle("audio")}
                    />
                    <span className="text-sm text-slate-700">Audio file</span>
                  </label>
                  <label className="flex items-center gap-3">
                    <Checkbox
                      checked={shareSelection.modelConfig}
                      onChange={() => handleShareToggle("modelConfig")}
                    />
                    <span className="text-sm text-slate-700">Model configuration</span>
                  </label>
                  <label className="flex items-center gap-3">
                    <Checkbox
                      checked={shareSelection.reviewerNotes}
                      onChange={() => handleShareToggle("reviewerNotes")}
                    />
                    <span className="text-sm text-slate-700">Reviewer notes</span>
                  </label>
                </div>
              </div>

              {/* Purpose */}
              <div className="mb-5">
                <h3 className="text-sm font-medium text-slate-800 mb-2">
                  Purpose
                </h3>
                <select
                  value={purpose}
                  onChange={(e) => setPurpose(e.target.value)}
                  className="w-full rounded-lg border border-slate-200 p-2 text-sm"
                >
                  {shareOptions.purposes.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Retention */}
              <div className="mb-5">
                <h3 className="text-sm font-medium text-slate-800 mb-2">
                  Retention period
                </h3>
                <select
                  value={retention}
                  onChange={(e) => setRetention(e.target.value)}
                  className="w-full rounded-lg border border-slate-200 p-2 text-sm"
                >
                  {shareOptions.retentions.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Privacy notice */}
              <div className="mb-5 p-3 bg-slate-50 rounded-lg border border-slate-200">
                <p className="text-xs text-slate-600">
                  <strong>Note:</strong> Shared cases will be accessible to recipients 
                  according to the retention period selected. Audio files may contain 
                  personal data - ensure you have proper consent before sharing.
                </p>
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  className="flex-1"
                  onClick={() => setDrawerOpen(false)}
                >
                  Cancel
                </Button>
                <Button className="flex-1" onClick={handleShare}>
                  Share
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
      </div>)}