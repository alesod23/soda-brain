"""The monitor layer (docs/MONITOR-LAYER.md): one event log per person, every channel, both directions.

SKELETON. Nothing in production imports this package yet.

    events.py       Event, StoredEvent, Finding, handle normalisation
    store.py        the Store interface, MemoryStore (tests, shadow dry runs), PgStore (brain.events)
    ingest.py       the Adapter interface, the Resolver (route memo first, then CRM), run_once()
    subscribers.py  the Subscriber interface, Dispatcher (path A), sweep() (path B), attribution()
    adapters/       one module per source; linkedin_store.py is the reference adapter
"""
