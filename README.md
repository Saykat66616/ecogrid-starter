# EcoGrid Energy

Peer-to-peer renewable energy trading: homeowners with solar panels sell surplus
electricity to their neighbours. This repository is the architecture starter that
accompanies the System Design Report. It is a working walking skeleton, not a
production system: the domain logic, the context boundaries and the fitness
functions are real; Kafka, PostgreSQL and the cloud are replaced by in-memory
stand-ins behind the same ports.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

python run_demo.py               # end-to-end demo: readings -> trades -> settled ledger
pytest                           # unit tests and fitness functions
pytest -m fitness                # fitness functions only
```

The checks CI runs (macOS/Linux shown; on Windows PowerShell use `$env:PYTHONPATH="services;libs"`):

```bash
export PYTHONPATH=services:libs
ruff check . && ruff format --check .
mypy
lint-imports
pytest --cov
bandit -q -r services libs composition -x '*/tests/*'
```

## Layout

```text
services/
  metering/       Smart Meter Integration: validate, dedupe, window readings into 5-minute intervals
  marketplace/    Marketplace: offers, bids, price-time matching, surplus projection, HTTP API
  settlement/     Financial Settlement: double-entry ledger, settlement saga, payouts
    domain/         pure business rules, no I/O
    application/    use cases and ports
    adapters/       HTTP, vendor formats, external providers
    tests/
libs/
  ecogrid_contracts/   Shared Kernel: units and event schemas (the Published Language)
  ecogrid_platform/    paved-road helpers: event bus port, inbox for idempotency
composition/           the only place that imports all three contexts: wiring and demo
tests/fitness/         architectural fitness functions
docs/adr/              architecture decision records
.github/               CI pipeline and CODEOWNERS
```

## The rules this repository enforces

1. A bounded context never imports another bounded context. Contexts share only
   the events in `libs/ecogrid_contracts`.
2. Inside a context, dependencies point inwards: adapters -> application -> domain.
3. Event schemas change only in backward-compatible ways.
4. The ledger always balances, and every entry traces to a trade or a top-up.
5. Every event handler is idempotent; the demo and the fitness tests deliver
   every event twice to prove it.

Break rule 1 on purpose (add `import settlement` to a Marketplace file) and run
`pytest -m fitness` to see the build fail.

## From skeleton to production

| Stand-in here | Production replacement | Port to implement |
| --- | --- | --- |
| `InMemoryEventBus` | Managed Kafka with a schema registry | `EventPublisher` |
| In-memory dictionaries in services | PostgreSQL / TimescaleDB repositories with a transactional outbox | repository ports per context |
| `FakePaymentProvider` | Real payment provider adapter | `PaymentPort` |
| Direct `ingest()` calls | MQTT gateway feeding a Kafka consumer | `IngestionService` |

## Team workflow

- Short-lived branches, pull requests, at least one review; CODEOWNERS routes reviews.
- Significant decisions are recorded in `docs/adr`.
- Update `.github/CODEOWNERS` with your GitHub usernames.
