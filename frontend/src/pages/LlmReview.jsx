import { useState } from "react";
import { Card, CardHeader } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { llmCases } from "../mocks/llmReviewCases";

const scoreLabels = ["Poor", "Fair", "Good"];

const criteria = [
  { key: "correctness", label: "Correctness", description: "Is the response factually accurate?" },
  { key: "groundedness", label: "Groundedness", description: "Is the response based on the source context?" },
  { key: "appropriateBehavior", label: "Appropriate behavior", description: "Is the response safe and appropriate?" },
  { key: "instructionFollowing", label: "Instruction following", description: "Does the response follow the user's instructions?" },
];

export default function LlmReview() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [scores, setScores] = useState(llmCases.map(() => ({
    correctness: null,
    groundedness: null,
    appropriateBehavior: null,
    instructionFollowing: null,
  })));
  const [notes, setNotes] = useState(llmCases.map(() => ""));

  const currentCase = llmCases[currentIndex];

  const handleScoreChange = (criteriaKey, value) => {
    const newScores = [...scores];
    newScores[currentIndex][criteriaKey] = value;
    setScores(newScores);
  };

  const handleNotesChange = (value) => {
    const newNotes = [...notes];
    newNotes[currentIndex] = value;
    setNotes(newNotes);
  };

  const handlePrevious = () => {
    if (currentIndex > 0) setCurrentIndex(currentIndex - 1);
  };

  const handleNext = () => {
    if (currentIndex < llmCases.length - 1) setCurrentIndex(currentIndex + 1);
  };

  const handleSave = () => {
    console.log("Saved case:", currentCase.id, scores[currentIndex], notes[currentIndex]);
    alert("Review saved!");
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">LLM Review</h1>
          <p className="text-sm text-slate-500">
            Evaluate LLM responses for quality and accuracy.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="secondary" onClick={handlePrevious} disabled={currentIndex === 0}>
            ← Previous
          </Button>
          <span className="text-sm text-slate-600">
            Case {currentIndex + 1} of {llmCases.length}
          </span>
          <Button variant="secondary" onClick={handleNext} disabled={currentIndex === llmCases.length - 1}>
            Next →
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-5">
        {/* Main content - 2 columns */}
        <div className="col-span-2 space-y-5">
          {/* Chat bubbles */}
          <Card>
            <CardHeader title="Conversation" />
            <div className="space-y-4">
              {currentCase.conversation.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-start" : "justify-end"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      msg.role === "user"
                        ? "bg-slate-100 text-slate-800"
                        : "bg-indigo-600 text-white"
                    }`}
                  >
                    <p className="text-xs font-medium mb-1 opacity-75">
                      {msg.role === "user" ? "User" : "Assistant"}
                    </p>
                    <p className="text-sm">{msg.content}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Scoring criteria */}
          <Card>
            <CardHeader title="Quality Assessment" />
            <div className="space-y-4">
              {criteria.map((criterion) => (
                <div key={criterion.key}>
                  <div className="mb-2">
                    <p className="text-sm font-medium text-slate-800">{criterion.label}</p>
                    <p className="text-xs text-slate-500">{criterion.description}</p>
                  </div>
                  <div className="flex gap-4">
                    {[0, 1, 2].map((value) => (
                      <label key={value} className="flex items-center gap-2">
                        <input
                          type="radio"
                          name={`${currentCase.id}-${criterion.key}`}
                          checked={scores[currentIndex][criterion.key] === value}
                          onChange={() => handleScoreChange(criterion.key, value)}
                          className="h-4 w-4 text-indigo-600"
                        />
                        <span className="text-sm text-slate-700">
                          {value} - {scoreLabels[value]}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Notes */}
          <Card>
            <CardHeader title="Reviewer Notes" />
            <textarea
              className="w-full rounded-lg border border-slate-200 p-3 text-sm"
              rows={4}
              placeholder="Add your comments here..."
              value={notes[currentIndex]}
              onChange={(e) => handleNotesChange(e.target.value)}
            />
            <Button className="mt-3" onClick={handleSave}>
              Save Review
            </Button>
          </Card>
        </div>

        {/* Sidebar - 1 column */}
        <div className="space-y-5">
          {/* Source context */}
          <Card>
            <CardHeader title="Source Context" />
            <p className="text-sm text-slate-700">{currentCase.sourceContext}</p>
          </Card>

          {/* Case details */}
          <Card>
            <CardHeader title="Case Details" />
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500">Model</span>
                <span className="font-medium">{currentCase.caseDetails.model}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Temperature</span>
                <span className="font-medium">{currentCase.caseDetails.temperature}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Tokens</span>
                <span className="font-medium">{currentCase.caseDetails.tokens}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Latency</span>
                <span className="font-medium">{currentCase.caseDetails.latency}</span>
              </div>
            </div>
          </Card>

          {/* Progress indicator */}
          <Card>
            <CardHeader title="Progress" />
            <div className="flex flex-wrap gap-2">
              {llmCases.map((_, i) => {
                const isComplete = scores[i].correctness !== null;
                return (
                  <Badge key={i} variant={isComplete ? "success" : "default"}>
                    {i + 1}
                  </Badge>
                );
              })}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}