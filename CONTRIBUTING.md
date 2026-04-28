# Contributing to Poliittinen Muisti

Thank you for helping track Finnish political accountability!

## How to Contribute

### 1. Add a Statement

Found a politician making a claim, prediction, or promise? Here's how to add it:

1. **Fork this repository**
2. **Create a transcript** (if not already present)
   - Use `python scripts/transcribe.py` for YouTube videos
   - Or manually create a markdown file in `transcripts/`
3. **Create a statement file** in `data/statements/`
   - Filename format: `{date}-{politician-slug}-{topic}-{number}.json`
   - Example: `2024-03-15-orpo-healthcare-001.json`
4. **Fill in all required fields** (see format below)
5. **Open a Pull Request**

### 2. Verify a Statement

Know the outcome of a prediction or claim? Help verify it:

1. **Find evidence** (official statistics, news reports, documents)
2. **Create a verification file** in `data/verifications/`
3. **Link to evidence** with URLs
4. **Assign a verdict** with reasoning
5. **Open a Pull Request**

### 3. Report a Contradiction

Found a politician saying opposite things?

1. **Find both statements** (must already be in the database, or add them)
2. **Create a contradiction file** in `data/contradictions/`
3. **Document if acknowledged** (did they explain the change?)
4. **Open a Pull Request**

---

## Data Formats

### Statement

```json
{
  "id": "2024-03-15-orpo-healthcare-001",
  "politician_id": "petteri-orpo",
  "statement": "Finnish text of statement",
  "statement_en": "English translation (optional but helpful)",
  "type": "prediction|factual_claim|promise|policy_position",
  "topic": ["healthcare", "budget"],
  "confidence": "high|medium|low|hedged",
  "reasoning": "Their justification (if given)",
  "date": "2024-03-15",
  "source_url": "https://...",
  "source_type": "tv_interview|parliament_speech|podcast|social_media|campaign_speech",
  "platform": "Yle|MTV3|Eduskunta|Twitter|etc",
  "transcript_file": "transcripts/filename.md",
  "timestamp_seconds": 340,
  "submitted_by": "your-github-username",
  "status": "pending"
}
```

### Verification

```json
{
  "id": "ver-xxx",
  "statement_id": "2024-03-15-orpo-healthcare-001",
  "outcome": "What actually happened (Finnish)",
  "outcome_en": "English translation",
  "verdict": "correct|mostly_correct|mixed|mostly_incorrect|incorrect|unverifiable",
  "verdict_reasoning": "Why this verdict",
  "evidence": [
    {"url": "https://...", "description": "Source description", "type": "official_statistics|news_report|expert_analysis"}
  ],
  "outcome_date": "2025-03-15",
  "verified_by": "your-github-username",
  "review_status": "pending"
}
```

### Contradiction

```json
{
  "id": "con-xxx",
  "politician_id": "petteri-orpo",
  "topic": ["education"],
  "statement_a": {
    "id": "statement-id-1",
    "text": "Original statement",
    "date": "2023-01-15",
    "source_url": "https://..."
  },
  "statement_b": {
    "id": "statement-id-2",
    "text": "Contradicting statement",
    "date": "2024-06-20",
    "source_url": "https://..."
  },
  "acknowledged": false,
  "acknowledgment_details": "If acknowledged, what they said",
  "severity": "minor|moderate|major",
  "notes": "Context about the contradiction",
  "submitted_by": "your-github-username",
  "status": "pending"
}
```

---

## Guidelines

### Be Fair
- Same standards for all politicians, regardless of party
- Include full context, not cherry-picked quotes
- Link to original sources

### Be Accurate
- Double-check dates and quotes
- Use official translations when available
- Note uncertainty if present

### Be Respectful
- Focus on statements and outcomes, not personal attacks
- Describe, don't editorialize
- Let the data speak

---

## Review Process

1. **Automated checks** — JSON validation, required fields
2. **Community review** — Other contributors can comment on PRs
3. **Maintainer approval** — Final merge

Disputed verifications will be marked as such and can be discussed in issues.

---

## Questions?

Open an issue or start a discussion!
