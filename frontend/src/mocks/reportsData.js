export const reportCase = {
  id: "RPT-001",
  caseId: "LM-001",
  createdAt: "2025-01-15T10:30:00Z",
  reference: "Il y a dix-huit ans que Jean Valjean fut condamné.",
  modelPrediction: "Il y a dix ans que Jean Valjean fut condamné.",
  wer: 7.1,
  reviewerNotes: "La prédiction est presque correcte mais manque le mot 'huit'. Le modèle a probablement mal entendu le nombre.",
  modelConfig: {
    model: "whisper-large-v3",
    language: "fr",
    temperature: 0.2,
  },
  audioFile: "lesmis_0001.wav",
  audioDuration: "00:12",
  status: "Reviewed",
};

export const shareOptions = {
  purposes: [
    { value: "internal", label: "Internal review" },
    { value: "research", label: "Research publication" },
    { value: "training", label: "Model training" },
    { value: "demo", label: "Demo/Presentation" },
  ],
  retentions: [
    { value: "30d", label: "30 days" },
    { value: "90d", label: "90 days" },
    { value: "1y", label: "1 year" },
    { value: "permanent", label: "Permanent" },
  ],
};