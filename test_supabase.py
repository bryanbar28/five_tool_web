from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    data = supabase.table('users').select('*').execute()
    print("Connection successful! Users table data:", data.data)
except Exception as e:
    print("Connection failed:", str(e))