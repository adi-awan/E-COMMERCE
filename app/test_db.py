from core.supabase import supabase
from core.supabase import SUPABASE_URL

print("URL:", SUPABASE_URL)

result = supabase.table("products").select("*").execute()

print(result.data)