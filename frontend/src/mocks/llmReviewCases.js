export const llmCases = [
  {
    id: "LLM-001",
    conversation: [
      { role: "user", content: "Quel est le nom du personnage principal des Misérables ?" },
      { role: "assistant", content: "Le personnage principal des Misérables est Jean Valjean." },
    ],
    sourceContext: "Extrait du chapitre 3, Livre 1 : Jean Valjean sort de prison après 19 ans.",
    caseDetails: {
      model: "gpt-3.5-turbo",
      temperature: 0.7,
      tokens: 45,
      latency: "1.2s",
    },
    scores: {
      correctness: null,
      groundedness: null,
      appropriateBehavior: null,
      instructionFollowing: null,
    },
    notes: "",
  },
  {
    id: "LLM-002",
    conversation: [
      { role: "user", content: "Que fait Cosette dans cette scène ?" },
      { role: "assistant", content: "Cosette puise de l'eau à la fontaine. Elle semble fatiguée mais courageuse." },
    ],
    sourceContext: "Extrait du chapitre 7, Livre 3 : Cosette va chercher de l'eau à la fontaine.",
    caseDetails: {
      model: "gpt-3.5-turbo",
      temperature: 0.7,
      tokens: 52,
      latency: "1.5s",
    },
    scores: {
      correctness: null,
      groundedness: null,
      appropriateBehavior: null,
      instructionFollowing: null,
    },
    notes: "",
  },
  {
    id: "LLM-003",
    conversation: [
      { role: "user", content: "Pourquoi Javert poursuit-il Jean Valjean ?" },
      { role: "assistant", content: "Javert poursuit Jean Valjean car il est un inspecteur de police déterminé à faire respecter la loi, et Valjean est un forçat évadé." },
    ],
    sourceContext: "Extrait du chapitre 12, Livre 4 : Javert découvre l'identité de Monsieur Madeleine.",
    caseDetails: {
      model: "gpt-3.5-turbo",
      temperature: 0.7,
      tokens: 68,
      latency: "1.8s",
    },
    scores: {
      correctness: null,
      groundedness: null,
      appropriateBehavior: null,
      instructionFollowing: null,
    },
    notes: "",
  },
];