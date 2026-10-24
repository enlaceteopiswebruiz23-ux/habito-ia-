import os
from supabase import create_client

_client = None


def get_supabase():
    """Cliente único de Supabase (se crea la primera vez que se usa)."""
    global _client
    if _client is None:
        _client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    return _client
