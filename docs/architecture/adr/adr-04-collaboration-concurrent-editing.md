# ADR-04: Collaboration and Concurrent Editing Approach

- Status: draft
- Owner: Omar
- Date: TBD

## Context
Group officers can hand off draft posts to each other before publishing (see scope draft).
How does the system handle two people editing/publishing the same draft concurrently in
Assignment 2 (e.g. WebSockets for live co-editing, locking, last-write-wins with warnings)?

## Alternatives considered
1. Optimistic concurrency (last write wins, warn on conflict)
2. Pessimistic locking (one active editor at a time)
3. Real-time collaborative editing (WebSocket-synced, e.g. CRDT/OT)

## Decision
_(Which option was chosen and why.)_

## Consequences
_(Trade-offs, risks, what this enables/blocks for later assignments.)_
