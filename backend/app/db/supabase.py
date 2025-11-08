import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Singleton instance
supabase: Client = get_supabase_client()