# Technical Architecture / Decisions

## Data model

- `numbers` is the canonical telephone number, `UNIQUE(number)` with its core and snapshot of attributes/rule matches.
- `offers` is a seller listing with `source + external_id` uniqueness. Several offers can point to one number. The same number is not a synonym for the same seller listing.
- `career_scores` materializes one `(number_id, career_id)` row per career for fast filtering; index `(career_id, score DESC, number_id)`.
- `import_logs` stores filename, source, claimed permission basis, timestamp and row counts.

## Match calculations

Source of truth is the JSON rulebook+matrix. Core is `phone[2:]` (8 digits), adjacent pair extraction produces seven pairs. Every pair rule adds static attribute deltas to a baseline of 50. Each attribute is clamped 0–100, then weighted by profile weights. No AI-generated numeric interpretation.

**Known limitations:** The demo rules are not academically validated; scores are not probability estimates, performance metrics, nor predictive models. Opaque phone datasets must not be inferred to be authorized. Demo status `available` is fabricated and cannot be used as an actual inventory claim.

## API

- `GET /api/health`: heartbeat.
- `GET /api/meta`: versioned rules, weights, careers.
- `GET /api/stats`: counts and latest imports.
- `POST /api/analyze`: one number and optional career context.
- `POST /api/search`: ranked results, server-side filters, pagination.
- `POST /api/import/text`: bulk pasted phone-number extraction from authorized text, no prices inferred.
- `POST /api/import`: CSV upload + permission basis. Optional `X-Admin-Token` if `NI_IMPORT_TOKEN` configured; **do not deploy publicly without auth**.
- `/api/docs`: generated OpenAPI interface.

## Scale / performance

The MVP uses SQLite WAL with transactions and normalized keys. It avoids computing scores for all numbers on every search by precomputing career rows during import. A 100k-row import is synchronous and may take time; background workers and ingestion chunks are needed before claiming production throughput. Search filters such as `LIKE '%..%'` can degrade for millions of numbers. Migrate to indexed substring search, materialized filters and PostgreSQL when validated by benchmarks.

## Data/legal boundary

Import only seller-published inventory from authorized partners, feeds, licenses, or owned datasets. Require documentation of terms. Phone numbers that identify natural persons may be personal data. Never republish an arbitrary source database. Design data retention and deletion workflows if expanding to customer identities.
