"""Laptop-only shim: when Windows Application Control blocks psycopg's binary pq.pyd, fall back to the
pure-Python implementation with the libpq.dll that ships inside the `pgserver` package. The box (Linux)
never needs this. Sets nothing when the normal import works."""
import os
import sys


def _psycopg_imports() -> bool:
    try:
        import psycopg  # noqa: F401
        return True
    except ImportError:
        for m in [m for m in sys.modules if m.startswith("psycopg")]:
            del sys.modules[m]
        return False


if os.name == "nt" and not _psycopg_imports():
    try:
        import pgserver
        pq_dir = os.path.join(os.path.dirname(pgserver.__file__), "pginstall", "bin")
        if os.path.isfile(os.path.join(pq_dir, "libpq.dll")):
            os.environ["PATH"] = pq_dir + os.pathsep + os.environ.get("PATH", "")
            os.environ["PSYCOPG_IMPL"] = "python"
            os.add_dll_directory(pq_dir)
            if _psycopg_imports():
                print(f"[conftest] psycopg binary blocked; using pure-Python psycopg with {pq_dir}\\libpq.dll")
    except ImportError:
        pass
