# Hallucination Reduction Notes (Suits Legal AI)

This document captures what was actually wrong in this project, what was fixed, and how to reason about hallucination reduction in RAG systems.

## 1) What I Observed

From your test chats, the system showed these symptoms:

- Donna sometimes returned refusal text:
  - "I cannot provide legal advice..."
- Mike said:
  - "I've got nothing in my memory..."
  even when memory had documents.
- Harvey/Louis/Jessica still produced confident legal-sounding output even when research quality was weak.

This is a classic "RAG + agent pipeline mismatch" problem: retrieval and generation states were not aligned.

## 2) Root Causes Found

## A) Jurisdiction detection was brittle

Old logic in Mike used only Donna facts:

- If `"india"` in `facts.lower()` -> India
- Else -> New York

If Donna output was weak/refusal/ambiguous, Mike defaulted to New York and searched wrong chunks.

## B) Typos in user query broke routing

Example: `inda` instead of `india`.

This prevented simple keyword jurisdiction detection from matching India.

## C) Retrieved docs and final text could conflict

Even when retrieval returned docs, Mike's LLM response could still include a "got nothing" sentence.

So retrieval truth != model narrative.

## D) Missing structured intake when Donna refused

Donna refusal text gave poor downstream context. That made the pipeline fragile because agents assumed valid structured facts.

## E) Memory source consistency was unclear

There were multiple loading patterns, and the practical goal was to use exactly 3 PDFs. Without a single rebuild flow, behavior can look inconsistent.

## 3) Fixes Implemented

## A) Stronger memory path resolution

In `agents/mike.py`:

- Added `_resolve_memory_path()` with priority:
  1. `CHROMA_DB_PATH` (env)
  2. `data/mikes_brain`
  3. legacy fallback `data/mike_brain` if legacy has existing DB

Why this helps:
- Prevents "reading from wrong DB path" errors that look like hallucination.

## B) Better jurisdiction inference

In `agents/mike.py`:

- Added `_detect_jurisdiction(query, facts)` using both query + facts.
- Added India hint terms including typo-tolerant terms (`inda`, `fir`, etc.).

Why this helps:
- Retrieval is routed to the right legal corpus more often.

## C) Jurisdiction-aware retrieval filter

In `agents/mike.py`:

- Retrieval now first tries metadata filter:
  - `filter={"jurisdiction": jurisdiction}`
- Falls back to unfiltered retrieval for older chunks missing metadata.

Why this helps:
- Reduces cross-jurisdiction contamination (e.g., New York chunks for India complaints).

## D) Donna refusal fallback

In `agents/Donna.py`:

- If model returns refusal text, create a structured intake fallback with:
  - legal issue
  - jurisdiction guess
  - opposing party
  - urgency

Why this helps:
- Downstream agents always get usable structure.

## E) Mike "no memory" contradiction guard

In `agents/mike.py`:

- Prompt instruction now explicitly forbids saying "I've got nothing in my memory" when memory items were found.

Why this helps:
- Reduces contradictory responses.

## F) Rebuilt RAG corpus from exactly 3 PDFs

In `load_india_police.py`:

- Rebuild script now:
  - clears existing collection
  - indexes exactly:
    - `policeact.pdf`
    - `policemanual.pdf`
    - `tenants.pdf`
  - writes jurisdiction metadata per source

Why this helps:
- Deterministic memory base for testing and learning.

## 4) What Was Verified

These checks were run after changes:

- Mike vectorstore loads and returns chunk count.
- Rebuild completed with expected chunk totals.
- Query similar to:
  - `police aint taking my compalint in inda`
  returned India-related memory results.
- Donna fallback produced structured intake with `JURISDICTION: India`.
- Mike output no longer included contradictory "got nothing" when docs were retrieved.

## 5) Practical Anti-Hallucination Lessons (General RAG)

1. Retrieval and generation must be tightly coupled.
   - If no docs -> explicit no-answer mode.
   - If docs exist -> force citation-only mode.

2. Metadata is not optional.
   - Store fields like jurisdiction/source/date/type.
   - Use metadata filters before semantic search fallback.

3. User input is noisy.
   - Handle typos, abbreviations, slang.
   - Do not rely on one exact keyword.

4. Agent pipelines need guardrails at each stage.
   - Intake fallback
   - Retrieval confidence threshold
   - Strategy agents blocked from inventing legal citations

5. Always keep a reproducible indexing workflow.
   - One command/script to rebuild corpus.
   - Deterministic source list for debugging.

## 6) Remaining Risk (Important)

Even with these improvements, LLMs can still produce fluent but weak claims.

For stronger reliability, add these next:

- Evidence gating:
  - Harvey/Louis/Jessica should only act on explicit cited snippets from Mike.
- Minimum retrieval score threshold:
  - If relevance too low, force "insufficient evidence."
- Structured citations:
  - Attach source + chunk IDs in Mike output.
- Optional reranker:
  - Re-rank top chunks before final synthesis.

## 7) Suggested Self-Study Exercises

1. Change one user prompt typo and observe jurisdiction detection behavior.
2. Remove jurisdiction filter and compare answer drift.
3. Index only one PDF and test how often agents over-generalize.
4. Add a fake irrelevant PDF and test whether metadata filtering blocks contamination.
5. Build a "strict mode" where non-cited sentences are automatically rejected.

## 8) File References for Study

- `agents/mike.py` - retrieval, jurisdiction, memory path logic
- `agents/Donna.py` - intake fallback behavior
- `load_india_police.py` - deterministic corpus rebuild flow
- `data/case_law/` - source documents
- `data/mikes_brain/` - persisted vector memory

---

If you want, the next study note I can create is a **step-by-step diagram of the full data flow** (User -> Donna -> Mike retrieval -> strategy agents), with exactly where hallucination can enter and how to test each boundary.

