# SKILLS.md — cl_mail_assistant_mooon / Mail Assistant → future Omnichannel Assistant

## 1. Project identity

Project name: cl_mail_assistant_mooon.

Current product stage: Mail Assistant for incoming e-mail processing.

Future product direction: Omnichannel Assistant. The architecture should not block future expansion into other inbound channels, but the current MVP is strictly e-mail-native.

The current system automates primary understanding and handling of incoming e-mails in the shared mailbox info@mooon.by.

This is not just an AI wrapper. It is not just a draft generator. It is a modular, case-driven, operator-assisted processing system for inbound messages.

The system should work around solving the incoming case correctly, not around simply generating text.

Main goals:

- understand incoming e-mails;
- normalize and preserve the message;
- extract attachments and useful text from them;
- enrich the message with factual context;
- bind the message to a case/thread;
- produce structured LLM understanding;
- retrieve relevant stable knowledge;
- support a later decision layer;
- support safe draft building;
- show the operator clear context and suggested handling;
- preserve auditability and inspectability at every stage.

## 2. Current channel model

Current customer channel: e-mail only.

Current inbound mailbox: info@mooon.by.

Current internal operator channel: Telegram as operator control plane.

Telegram is not a customer channel at this stage. It is only an internal operator interface for case cards, decisions and actions.

Future omnichannel direction may include other customer channels, but do not design or implement them in the current Mail Assistant MVP unless explicitly requested.

## 3. Brand and mailbox identity

The operational context is mooon cinema network.

Relevant brands and services:

- mooon;
- SilverScreen;
- go2.by.

Relevant cinema locations:

- mooon в Dana Mall;
- mooon в Palazzo;
- mooon в ArenaCity;
- mooon в Trinity Гродно.

Do not describe info@mooon.by as a Cinemalab inbox in project identity prompts or customer-facing context.

Cinemalab may be the company behind development, but the project identity for LLM context is the mooon shared incoming mailbox.

## 4. What kind of mailbox this is

info@mooon.by is not only a support mailbox.

It is a general incoming mailbox for the cinema network.

Therefore the core classification is not support / not support.

The correct operational question is: needs processing / can be safely ignored.

Meaningful e-mails must not be automatically ignored.

Meaningful incoming messages include:

- customer questions;
- refund questions;
- ticket questions;
- payment problems;
- questions about schedule;
- questions about repertoire;
- partner offers;
- advertising and marketing proposals;
- letters from government bodies;
- documents from counterparties;
- acts;
- invoices;
- contracts;
- legal documents;
- operational service notifications requiring action.

no_reply / ignore is allowed only for clearly safe cases:

- obvious spam;
- irrelevant mass sales;
- pure bounce / undelivered messages;
- MAILER-DAEMON messages;
- automatic service notifications with no required action;
- duplicates;
- technical noise.

If an e-mail is meaningful or may require business action, do not ignore it.

## 5. Product principle

The system must work around correct handling of a case, not around writing a reply.

The main unit is not just a single message.

The intended unit is case / thread with state, history and processing route.

Even when the MVP processes single messages, the architecture must remain case-aware and thread-aware.

The system is:

- e-mail-native at current MVP stage;
- modular;
- stateful;
- operator-assisted;
- inspectable;
- suitable for later omnichannel expansion.

## 6. Current accepted pipeline status

Already implemented and accepted:

1. mail_import
2. attachment_extraction
3. identity_context_enrichment
4. case_thread_binding
5. Structured LLM Understanding

Current active block:

- Knowledge Base MVP;
- then Knowledge Retrieval MVP.

Do not jump to Decision Layer, Draft Builder, Telegram operator card or reply sending before Knowledge Retrieval MVP is designed, implemented and tested.

## 7. Target pipeline

Target pipeline:

1. mail_import
2. attachment_extraction
3. identity_context_enrichment
4. case_thread_binding
5. structured_llm_understanding
6. knowledge_retrieval
7. decision_layer
8. draft_builder
9. telegram_operator_delivery
10. operator_actions
11. reply_sender
12. audit_metrics

Each step must remain a separate module with separate responsibility, separate runner and inspectable output.

## 8. Module architecture principle

Do not build a monolithic script.

Each pipeline step must have:

- clear responsibility;
- clear input;
- clear output;
- inspectable artifacts;
- separate runner;
- isolated testing mode.

The orchestrator must not replace the module structure. It only runs already accepted modules together.

Work must move step by step:

- design one module;
- implement one module;
- test one module;
- inspect artifacts and logs;
- accept the module;
- only then move to the next module.

No big bang.

## 9. Main runners and live flow

Current main live entrypoint:

- src/runners/run_mail_import_poller.py

This is the main operational intake flow and runs continuously in the background.

Secondary one-shot runner:

- src/runners/run_mail_import.py

run_mail_import.py mirrors the import behavior for single execution but is not the main live flow.

For new modules, create separate lab/runner entrypoints before wiring them into the full pipeline.

## 10. Main artifact model

The main per-message dossier artifact is:

- message_<uid>.md

The project intentionally moved away from excessive scattered JSON files.

Preferred artifact approach:

- one main human-readable and machine-readable dossier per message;
- raw e-mail stored separately;
- attachments stored next to the message artifacts;
- extracted attachment text stored next to the message artifacts;
- module outputs appended into the dossier.

The dossier already contains:

- human-readable section: LLM Understanding;
- machine payload: modules.llm_understanding.

Future Knowledge Retrieval must add:

- human-readable section: Knowledge Retrieval;
- machine payload: modules.knowledge_retrieval.

## 11. Mail Import principles

mail_import is not just fetching mail.

It performs safe intake and normalization.

It should extract maximum technical information from the message itself before external lookup:

- Message-ID;
- In-Reply-To;
- References;
- subject;
- from;
- to;
- date;
- raw headers;
- body_text;
- body source selection;
- presence of text/plain and text/html;
- MIME parts breakdown;
- attachment inventory;
- technical flags.

Technical flags may include:

- is_bounce;
- is_auto_reply;
- is_mailing_like;
- is_system_generated_likely.

Each such flag should have explainable reasons.

## 12. Attachment Extraction principles

Attachments are first-class input.

They are not secondary decorations on the e-mail.

The system should as early as possible:

- see attachments;
- build attachment inventory;
- save allowed attachments;
- detect file types;
- extract text / OCR / structure where possible.

Important distinction:

- attachment inventory / intake;
- attachment extraction / OCR / parsing;
- semantic understanding of attachment content.

Not all attachment processing requires LLM.

LLM should receive already extracted technical and text content where possible.

## 13. Identity / Context Enrichment principle

Data lookup is not a separate route.

It is part of the early identity/context enrichment layer.

Factual context should be collected before LLM Understanding and before later decision-making.

The system should avoid making important decisions blindly.

Potential factual context:

- customer;
- orders;
- tickets;
- refunds;
- loyalty card;
- bonuses;
- previous cases;
- other factual lookup results.

## 14. Case / Thread Binding principle

A new e-mail should be treated as a move inside a dialogue when possible, not only as an isolated object.

The architecture must preserve:

- message;
- thread;
- case;
- Message-ID;
- In-Reply-To;
- References;
- subject;
- sender;
- date;
- our outgoing replies as part of case history.

MVP may stabilize single-message behavior first, but the structure must remain thread-aware and case-aware.

## 15. Structured LLM Understanding

Structured LLM Understanding is already implemented and accepted.

Its job is not to answer the customer.

Its job is to produce structured understanding of the prepared message context.

Input should include:

- message dossier;
- extracted attachment content;
- factual enrichment;
- case/thread context where available.

Expected output fields:

- summary;
- topic;
- customer_need;
- entities;
- confidence;
- response_mode.

response_mode is mandatory.

Allowed response modes:

- answer;
- ask_clarifying_question;
- handoff_to_operator;
- no_reply/ignore.

Optional service fields may include:

- risk_level;
- needs_human.

Structured LLM Understanding is not the final decision-maker. It prepares structured input for later layers.

## 16. Knowledge Base MVP purpose

Knowledge Base is the stable knowledge layer.

It stores manually controlled stable knowledge:

- rules;
- FAQ fragments;
- internal instructions;
- operator instructions;
- response template hints;
- regulations;
- later historical cases.

Knowledge Base is not:

- live lookup;
- a connector;
- a decision layer;
- a draft writer;
- a vector DB by default;
- schedule storage;
- a replacement for factual enrichment.

## 17. Knowledge Base storage decision

Preferred MVP storage:

- config/knowledge_base/knowledge_base.xlsx

Single XLSX workbook.

Do not use CSV split for the MVP unless the user explicitly reverses this decision.

The workbook should contain sheets:

- KB_ITEMS;
- KB_DICTIONARY;
- KB_TYPES;
- KB_SETTINGS.

Reason for one XLSX workbook:

- more visual;
- easier to inspect manually;
- easier to edit in Excel;
- less file clutter;
- better for business review;
- matches user preference.

Previous CSV split was rejected as not visual enough.

Broken GitHub PR attempts with XLSX should not be treated as reliable source if the local file is rebuilt.

For local work, create and verify a valid Excel file before committing.

## 18. KB_ITEMS sheet

Main knowledge item table.

Recommended columns:

- id;
- enabled;
- type;
- title;
- priority;
- topic_keywords;
- entity_keywords;
- customer_need_keywords;
- response_modes;
- applies_to;
- content;
- operator_instruction;
- template_hint;
- source;
- notes.

Meaning:

- id: stable unique knowledge item ID;
- enabled: whether the item is active;
- type: rule / faq / operator_instruction / response_template / regulation / historical_case;
- title: short readable title;
- priority: manual priority for ranking;
- topic_keywords: keywords matching LLM topic;
- entity_keywords: keywords matching extracted entities;
- customer_need_keywords: keywords matching customer need;
- response_modes: response modes where this item may apply;
- applies_to: customer / partner / government / counterparty / system / spam;
- content: main stable knowledge;
- operator_instruction: internal handling instruction;
- template_hint: possible wording hint for future Draft Builder;
- source: source of the rule;
- notes: internal notes.

## 19. KB_DICTIONARY sheet

Dictionary of normalized entities, aliases and synonyms.

Recommended columns:

- entity_id;
- type;
- canonical_value;
- aliases;
- notes.

Purpose:

- normalize brand names;
- normalize venue names;
- normalize common intents;
- improve matching without embeddings.

Examples:

- mooon / moon / мун → mooon;
- go2 / go2.by / го2 → go2.by;
- Dana Mall / дана / mooon dana → mooon в Dana Mall.

## 20. KB_TYPES sheet

Controlled list of knowledge item types.

Recommended columns:

- type;
- enabled;
- description.

Supported MVP types:

- rule;
- faq;
- operator_instruction;
- response_template;
- regulation.

Reserved for later:

- historical_case.

## 21. KB_SETTINGS sheet

Simple settings for MVP retrieval.

Recommended columns:

- key;
- value;
- description.

Possible settings:

- min_score;
- max_results;
- enabled_types;
- no_result_behavior;
- source_format.

Default behavior:

- no_result_behavior = return_empty.

If nothing is found, Retrieval must return empty result and must not invent context.

## 22. First Knowledge Base seed topics

Initial KB must stay small.

Do not overfill the database before Retrieval MVP is tested.

First seed topics:

- refund_policy;
- ticket_not_received_policy;
- schedule_question_policy;
- bounce_policy.

These are enough to test:

- normal customer support case;
- ticket recovery case;
- dynamic schedule/repertoire case;
- no_reply / ignore case.

After retrieval flow is tested, return to broader KB filling.

## 23. Knowledge item type definitions

rule: processing rule explaining how to handle a class of messages.

faq: stable factual answer fragment for common questions.

operator_instruction: internal instruction for operator handling, not intended as direct customer-facing text.

response_template: reusable wording or template hint for future Draft Builder, not the final answer.

regulation: internal or external rule that constrains handling.

historical_case: reserved for later; do not implement in MVP unless explicitly requested.

## 24. Dynamic data separation

Important distinction:

Knowledge Base = stable knowledge.

Connector / live lookup = dynamic data.

Stable Knowledge Base examples:

- refund rules;
- instructions;
- FAQ;
- processing policies;
- operator guidance;
- template hints.

Dynamic data examples:

- current schedule;
- film sessions;
- prices;
- ticket availability;
- live repertoire;
- current seat availability.

Dynamic data must not be stored as static KB facts.

## 25. Schedule and repertoire handling

Potential future live source:

- https://rest.go2.by/static/media-storage/util/schedule/go2.xml

This is not Knowledge Base.

It belongs to a future Schedule Connector.

Correct logic:

1. Understanding detects that the customer asks about film / schedule / repertoire.
2. Retrieval finds schedule_question_policy.
3. Schedule Connector may later query go2.xml or another live source.
4. Decision Layer decides whether it can answer factually or must hand off.

For MVP without Schedule Connector:

- schedule / repertoire question → handoff_to_operator.

The system must not invent schedule facts from memory.

## 26. Knowledge Retrieval / RAG purpose

Knowledge Retrieval runs after Structured LLM Understanding.

It receives:

- message_<uid>.md;
- modules.llm_understanding;
- full dossier context where needed.

Its job:

- read the Knowledge Base;
- find relevant knowledge items;
- return matched knowledge fragments;
- write result into modules.knowledge_retrieval.

It must not:

- make final handling decisions;
- invent missing facts;
- answer the customer;
- draft replies;
- call live external systems;
- decide whether schedule data exists;
- replace Decision Layer.

Retrieval returns either matched knowledge items or empty result.

If nothing is found, it must return empty result and not hallucinate context.

## 27. Knowledge Retrieval MVP matching logic

For MVP, do not use vector DB.

Do not require embeddings.

Use simple inspectable matching.

Input:

- topic;
- customer_need;
- entities;
- response_mode;
- possibly summary.

Source:

- config/knowledge_base/knowledge_base.xlsx.

MVP matching:

1. Load workbook.
2. Read KB_ITEMS.
3. Filter enabled = yes.
4. Filter enabled types from KB_SETTINGS.
5. Normalize text using KB_DICTIONARY.
6. Match against topic_keywords, entity_keywords, customer_need_keywords, response_modes, applies_to.
7. Calculate simple explainable score.
8. Sort by score descending and priority descending.
9. Return top max_results.
10. If no score reaches min_score, return empty result.

The score must be explainable.

Retrieval result should include why an item matched.

## 28. Knowledge Retrieval output

Knowledge Retrieval output should be written into the dossier.

Human-readable section:

- Knowledge Retrieval;
- status;
- matched item count;
- matched item IDs;
- score;
- short match explanation.

Machine payload:

- modules.knowledge_retrieval.status;
- modules.knowledge_retrieval.matched_items;
- item id;
- item type;
- title;
- score;
- priority;
- matched_fields;
- content;
- operator_instruction;
- template_hint.

Possible statuses:

- found;
- empty;
- disabled;
- error.

If empty:

- status = empty;
- matched_items = empty list.

## 29. Knowledge Retrieval LAB

Future isolated runner:

- src/runners/run_knowledge_retrieval_lab.py

It should work similarly to the existing Structured Understanding lab.

Required behavior:

- show latest dossier messages;
- show UID / sender / subject / date if available;
- user selects a case by number;
- Enter repeats the last selected case;
- q exits;
- result writes next to lab artifacts.

Expected lab output files:

- knowledge_retrieval_lab_latest.json;
- knowledge_retrieval_lab_runs.jsonl.

The lab exists for repeated tuning of KB and retrieval logic on frozen e-mail dossiers.

## 30. Testing strategy

Test first in isolation.

Do not immediately wire into full pipeline.

First test Knowledge Retrieval on frozen dossiers that already have modules.llm_understanding.

Required test cases:

1. Refund case.
2. Ticket not received case.
3. Schedule / repertoire question.
4. Bounce / undelivered message.
5. Message with no relevant KB match.

Expected outcomes:

- refund → refund_policy;
- ticket missing → ticket_not_received_policy;
- schedule → schedule_question_policy;
- bounce → bounce_policy;
- unknown → empty result.

The goal is not perfect semantic retrieval.

The goal is:

- workbook loads;
- matching works;
- result is inspectable;
- empty result is safe;
- output is written correctly.

## 31. What not to do now

Do not implement now:

- vector database;
- embeddings;
- big RAG;
- historical case search;
- live schedule lookup;
- schedule connector;
- decision layer;
- draft builder;
- automatic reply sending;
- Telegram operator card;
- production orchestration;
- omnichannel customer channels.

Do not mix Retrieval with live lookup.

Do not let Retrieval make business decisions.

Do not let Retrieval write replies.

## 32. Future Decision Layer

Decision Layer comes after Knowledge Retrieval.

It receives:

- message dossier;
- structured understanding;
- retrieved knowledge;
- factual enrichment;
- case/thread context.

Its job:

- confirm or correct response_mode;
- decide whether the system can answer;
- decide whether clarification is needed;
- decide whether handoff is needed;
- produce reasoning summary for operator.

Decision Layer is not the same thing as Retrieval.

## 33. Future Draft Builder

Draft Builder comes after Decision Layer.

It should build a draft only from already prepared context:

- structured understanding;
- response_mode;
- retrieved knowledge;
- decision-layer result;
- factual enrichment where available.

Draft Builder must not answer from raw e-mail alone.

Draft Builder must not invent facts.

## 34. Operator role

Operator is not an emergency fallback.

Operator is a normal participant of the system.

Operator should see:

- case card;
- what was understood;
- factual context;
- retrieved knowledge;
- proposed route;
- draft where available;
- ability to confirm or change the system decision.

## 35. Development workflow rules

Default work style:

- be concise;
- do not invent missing facts;
- do not guess project structure;
- inspect actual current files before editing code;
- ask for actual files if needed;
- do not use Codex unless explicitly allowed;
- if a small change affects one or two files, handle directly;
- if larger, prepare detailed task first;
- do not change unrelated logic;
- do not introduce unsolicited architecture changes;
- do not create scattered artifacts when one clear file is enough.

When editing code for this user:

- use exact files;
- avoid broad rewrites;
- preserve current flow;
- show changes as было → стало when discussing code;
- if not asked to paste code, provide changed file or exact patch direction instead;
- do not suggest changing PyCharm Working Directory;
- remember that the user runs scripts from PyCharm using the Run button.

## 36. Console and logging preferences

Logs should be concise and readable.

For mail pipeline logs:

- English technical labels;
- one e-mail = one line where possible;
- no excessive timezone clutter;
- show useful fields only.

Preferred style:

uid, from, subject, attach summary, enrichment summary, binding summary, case, thread, rule, created yes/no.

Do not produce verbose noisy logs unless explicitly debugging.

## 37. Language rules

Technical logs and console labels: English.

End-user copy, operator-facing Russian UI/text and project explanations: Russian.

The user prefers direct Russian discussion.

Avoid unnecessary explanations.

## 38. Current immediate local plan

Current immediate task is to rebuild Knowledge Base locally as a valid workbook:

- config/knowledge_base/knowledge_base.xlsx.

Workbook sheets:

- KB_ITEMS;
- KB_DICTIONARY;
- KB_TYPES;
- KB_SETTINGS.

Then:

1. Open it in Excel and verify it is valid.
2. Remove old CSV files.
3. Update README.md.
4. Commit and push locally.
5. Move to Knowledge Retrieval MVP.

Do not continue using broken GitHub PR XLSX attempts as source of truth.

## 39. Future next module

After Knowledge Base workbook is valid, design and implement Knowledge Retrieval MVP.

Expected responsibility:

1. read knowledge_base.xlsx;
2. read modules.llm_understanding from message_<uid>.md;
3. find matching KB_ITEMS;
4. write modules.knowledge_retrieval.

It must be separately runnable and testable before being connected into the full orchestrator.
