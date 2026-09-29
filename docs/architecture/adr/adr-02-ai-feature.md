# ADR-02: AI Feature, Data Used, and Output Verification

- Status: draft
- Owner: Aro
- Date: TBD

## Context
Team agreed (2026-09-29): thread summarization — an LLM condenses a long comment thread into
a short digest. Aro to write up the full rationale, data used, and how a user verifies the
summary against the original thread.

## Alternatives considered
1. Thread summarization (chosen — clear, demoable, low risk if wrong)
2. Spam/toxicity flagging (rejected for this ADR — overlaps with moderation policy, ADR-01)
3.

## Decision
Thread summarization. Aro to detail: what triggers it, which model/data, and the UX for a
user to check the summary against the real thread (e.g. "view original" link, confidence note).

## Consequences
_(Trade-offs, risks, what this enables/blocks for later assignments.)_
