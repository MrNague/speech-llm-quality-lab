import { useState } from "react";
import { Card, CardHeader } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { AudioPlayer } from "../components/AudioPlayer";
import { DiffText } from "../components/DiffText";
import { asrSample } from "../mocks/asrAnalysisSample";

export default function AsrAnalysis() {
  const [severity, setSeverity] = useState("critical");

  return (
    <div className="p-6 space-y-5">
      <h1 className="text-xl font-semibold">ASR Analysis</h1>

      <div className="grid grid-cols-3 gap-5">
        <Card>
          <CardHeader title="Audio & Transcription" subtitle={asrSample.audio} />
          <AudioPlayer audioUrl={`/audio/${asrSample.audio}`} />
        </Card>

        <Card>
          <CardHeader title="Model & Run Settings" />
          <select className="mb-2 w-full rounded-lg border border-slate-200 p-2 text-sm">
            <option>whisper-large-v3 (local)</option>
          </select>
          <Button className="w-full justify-center">▶ Run ASR</Button>
        </Card>

        <Card>
          <CardHeader title="Metrics" />
          <div className="flex gap-6">
            <div>
              <p className="text-2xl font-semibold text-indigo-600">{asrSample.wer}%</p>
              <p className="text-xs text-slate-500">WER</p>
            </div>
            <div>
              <p className="text-2xl font-semibold text-slate-400">—</p>
              <p className="text-xs text-slate-500">CER</p>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-3 gap-5">
        <Card>
          <CardHeader title="Reference Transcript" />
          <p className="text-sm">{asrSample.reference}</p>
        </Card>

        <Card>
          <CardHeader title="ASR Prediction" />
          <p className="text-sm">{asrSample.prediction}</p>
        </Card>

        <Card>
          <CardHeader title="Word Comparison" />
          <DiffText reference={asrSample.reference} prediction={asrSample.prediction} />
        </Card>
      </div>

      <Card>
        <CardHeader title="Reviewer Assessment" />
        <div className="flex gap-4">
          {["no-error", "minor", "major", "critical"].map((v) => (
            <label key={v} className="flex items-center gap-1.5 text-sm">
              <input
                type="radio"
                name="severity"
                checked={severity === v}
                onChange={() => setSeverity(v)}
              />
              {v}
            </label>
          ))}
        </div>
        <Button className="mt-4">Save Review</Button>
      </Card>
    </div>
  );
}