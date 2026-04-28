# Knowledge Base MVP

This directory contains the first MVP version of the knowledge base for the `Knowledge Retrieval / RAG` layer.

## Purpose

Knowledge Retrieval is a technical pipeline step that runs after Structured LLM Understanding.
It does not make decisions and does not draft replies.
It only returns relevant stable knowledge for the next Decision Layer.

## Scope

This MVP stores stable knowledge only:

- processing rules;
- FAQ fragments;
- operator instructions;
- response template hints;
- regulations.

Dynamic data is intentionally out of scope:

- film schedule;
- session availability;
- prices;
- ticket availability;
- live lookup results.

Dynamic data must be handled later by dedicated connectors, for example a future Schedule Connector.

## Files

- `kb_items.csv` — main knowledge items table.
- `kb_dictionary.csv` — normalized entities, aliases and synonyms.
- `kb_types.csv` — controlled list of supported knowledge item types.
- `kb_settings.csv` — simple retrieval settings for MVP.

## Source of truth

For MVP, these CSV files are the source of truth.
A Google Sheet can be used later as a visual editor or mirror, but the pipeline should be able to read these files directly.

## Current MVP topics

The first seed topics are:

- `refund_policy`
- `ticket_not_received_policy`
- `schedule_question_policy`
- `bounce_policy`
