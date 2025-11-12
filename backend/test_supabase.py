import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Test both URLs
urls = [
    "postgresql://postgres:SmartSupport@db.uovtkfnnlypzcvgriehb.supabase.co:5432/postgres?sslmode=require",
    "postgresql://postgres:g7!R3qP#x9LmT2vB8zQw@db.rgkvblvvcguospltmvdm.supabase.co:5432/postgres"
]

for i, url in enumerate(urls, 1):
    print(f"Testing URL {i}...")
    try:
        conn = psycopg2.connect(url)
        print(f"✓ URL {i} works!")
        conn.close()
        break
    except Exception as e:
        print(f"✗ URL {i} failed: {e}")

print("\nIf both failed, try:")
print("1. Check Supabase project status")
print("2. Enable IPv6 on your network")
print("3. Use mobile hotspot temporarily")