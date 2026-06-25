# app/test_products.py

from app.core.supabase import supabase

response = supabase.table("products").select("*").execute()

print(response.data)