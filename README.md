# Poliittinen Muisti

> Track what Finnish politicians say, predict, and whether they were right.

**Open data. Open source. Full transparency.**

---

> **⚠️ DEMO DATA:** All current statements, verifications, and transcripts are **fictional examples** created to demonstrate the data structure. Real data collection has not started yet. Do not cite this as factual information about any politician.

---

## What This Is

A public database tracking:
- **What politicians say** — claims, predictions, promises
- **What actually happened** — outcomes, verified with evidence
- **Contradictions** — when they say one thing, then the opposite
- **Accuracy scores** — who's consistently right or wrong

All data lives in this repo. Every change is a git commit. Anyone can contribute via PR.

---

## Data Structure

```
data/
├── politicians/          # One JSON file per politician
│   └── {slug}.json
├── statements/           # Claims, predictions, promises
│   └── {date}-{slug}-{topic}.json
├── verifications/        # What actually happened
│   └── {statement-id}-verification.json
└── contradictions/       # Said X, then said not-X
    └── {politician}-{id}.json

transcripts/              # Full transcriptions
└── {date}-{source}.md
```

---

## Quick Stats

| Metric | Count |
|--------|-------|
| Politicians tracked | 3 (demo) |
| Statements | 5 (demo) |
| Verifications | 2 (demo) |
| Contradictions | 1 (demo) |

> **Note:** Current data is **fictional demo data** to illustrate the structure. Real data collection starts when we begin transcribing actual interviews.

---

## How to Contribute

### Add a new statement

1. Transcribe the source (or use `scripts/transcribe.py`)
2. Create a JSON file in `data/statements/`
3. Open a Pull Request

### Verify a statement

1. Find evidence of the outcome
2. Create a verification file linking to evidence
3. Open a Pull Request

### Report a contradiction

1. Find two conflicting statements from same politician
2. Create a contradiction file linking both
3. Open a Pull Request

---

## Data Formats

### Politician

```json
{
  "id": "petteri-orpo",
  "name": "Petteri Orpo",
  "party": "Kokoomus",
  "role": "Pääministeri",
  "eduskunta_id": "1234",
  "active": true
}
```

### Statement

```json
{
  "id": "2024-03-15-orpo-healthcare-001",
  "politician_id": "petteri-orpo",
  "statement": "Leikkaukset eivät vaikuta terveydenhuollon laatuun",
  "statement_en": "The cuts will not affect healthcare quality",
  "type": "prediction",
  "topic": ["healthcare", "budget"],
  "confidence": "high",
  "date": "2024-03-15",
  "source_url": "https://...",
  "source_type": "tv_interview",
  "transcript_file": "transcripts/2024-03-15-yle-interview.md"
}
```

### Verification

```json
{
  "id": "ver-001",
  "statement_id": "2024-03-15-orpo-healthcare-001",
  "outcome": "Healthcare wait times increased 40%",
  "verdict": "incorrect",
  "evidence": [
    {"url": "https://thl.fi/...", "description": "THL statistics"}
  ],
  "verified_date": "2025-03-15",
  "verified_by": "contributor-github-username"
}
```

### Contradiction

```json
{
  "id": "con-001",
  "politician_id": "petteri-orpo",
  "statement_a": {
    "text": "We will not cut education funding",
    "date": "2023-01-15",
    "source_url": "https://..."
  },
  "statement_b": {
    "text": "Education cuts are necessary",
    "date": "2024-06-20",
    "source_url": "https://..."
  },
  "acknowledged": false,
  "notes": "No acknowledgment of position change"
}
```

---

## Scoring

Scores are computed from the data:

| Metric | Formula |
|--------|---------|
| **Accuracy** | correct / (correct + incorrect) |
| **Contradiction Index** | contradictions / total statements |
| **Integrity Score** | acknowledged contradictions / total contradictions |

---

## Principles

1. **Non-partisan** — All politicians treated equally
2. **Evidence-based** — Every verification needs sources
3. **Transparent** — All data and history public
4. **Forkable** — Anyone can take the data elsewhere
5. **Correctable** — Mistakes can be fixed via PR

---

## Tools

### Transcribe a video

```bash
python scripts/transcribe.py "https://youtube.com/watch?v=..."
```

### Validate data

```bash
python scripts/validate.py
```

---

## License

- **Code**: MIT
- **Data**: CC BY 4.0 (use freely with attribution)

---

## See Also

- [Eduskunta Avoin Data](https://avoindata.eduskunta.fi/) — Parliament voting records
- [PolitiFact](https://www.politifact.com/) — US fact-checking

---

*Status: Early development with demo data*
