import { useState } from "react";
import { Card, CardHeader } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Checkbox } from "../components/ui/Checkbox";
import { AudioPlayer } from "../components/AudioPlayer";
import { examples } from "../mocks/dataQualityExamples";

export default function DataQuality() {
  const [selectedId, setSelectedId] = useState(examples[0].id);
  const selected = examples.find((e) => e.id === selectedId);

  return (
    <div className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Data Quality</h1>
          <p className="text-sm text-slate-500">
            Review and prepare development examples for speech and LLM evaluation.
          </p>
        </div>
        <Button variant="secondary">Design sample data</Button>
      </div>

      <div className="grid grid-cols-3 gap-5">
        <Card className="col-span-2">
          <CardHeader
            title={`Development examples (${examples.length})`}
            action={<Button>+ Add example</Button>}
          />
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs text-slate-500">
                <th className="py-2"><Checkbox /></th>
                <th>ID</th>
                <th>Category</th>
                <th>Reference (short preview)</th>
                <th>Validation</th>
                <th>Reviewer</th>
                <th>Ref. rev.</th>
              </tr>
            </thead>
            <tbody>
              {examples.map((ex) => (
                <tr
                  key={ex.id}
                  onClick={() => setSelectedId(ex.id)}
                  className={`cursor-pointer border-b border-slate-50 hover:bg-slate-50 ${
                    ex.id === selectedId ? "bg-indigo-50" : ""
                  }`}
                >
                  <td className="py-2"><Checkbox checked={ex.id === selectedId} readOnly /></td>
                  <td className="font-medium">{ex.id}</td>
                  <td><Badge variant="info">{ex.category}</Badge></td>
                  <td className="max-w-[220px] truncate text-slate-600">{ex.reference}</td>
                  <td><Badge variant="warning">{ex.validation}</Badge></td>
                  <td className="text-slate-500">{ex.reviewer}</td>
                  <td className="text-slate-500">{ex.refRev}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        <Card>
          <CardHeader title="Example details" subtitle={selected.id} />
          
          <p className="mb-1 text-xs font-medium text-slate-500">Audio file</p>
          <AudioPlayer audioUrl={`/audio/${selected.audio}`} />

          <p className="mb-1 mt-4 text-xs font-medium text-slate-500">Reference text (French)</p>
          <textarea
            className="w-full rounded-lg border border-slate-200 p-2 text-sm"
            rows={3}
            defaultValue={selected.reference}
          />

          <label className="mt-2 flex items-center gap-2 text-xs text-slate-600">
            <Checkbox /> Second listener review completed
          </label>

          <Button className="mt-4 w-full justify-center">Save reference revision</Button>
        </Card>
      </div>
    </div>
  );
}