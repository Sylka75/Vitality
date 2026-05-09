import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timezone

# Initialize connection
@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    supabase = None
    st.error(f"Failed to initialize Supabase. Check your secrets. {e}")

def get_user_profile():
    if not supabase: return None
    response = supabase.table("user_profile").select("*").eq("id", 1).execute()
    if response.data:
        return response.data[0]
    return None

def update_goal_calories(new_goal: int):
    if not supabase: return
    supabase.table("user_profile").update({"goal_calories": new_goal}).eq("id", 1).execute()

def update_next_day_goal(new_goal: int):
    if not supabase: return
    supabase.table("user_profile").update({"next_day_goal": new_goal}).eq("id", 1).execute()

def update_weight(new_weight: float):
    if not supabase: return
    # Update profile
    supabase.table("user_profile").update({"current_weight": new_weight}).eq("id", 1).execute()
    # Insert history
    today = datetime.now(timezone.utc).date().isoformat()
    supabase.table("weight_history").insert({"recorded_at": today, "weight_value": new_weight}).execute()

def get_weight_history():
    if not supabase: return []
    response = supabase.table("weight_history").select("*").order("recorded_at", desc=True).execute()
    return response.data

def insert_food_log(label: str, calories: int, emoji: str, raw_ai_suggestion: dict = None):
    if not supabase: return
    data = {
        "label": label,
        "calories": calories,
        "emoji": emoji,
        "raw_ai_suggestion": raw_ai_suggestion or {}
    }
    supabase.table("food_logs").insert(data).execute()

def get_today_food_logs():
    if not supabase: return []
    today = datetime.now(timezone.utc).date().isoformat()
    # Using gte and lte to filter by today in UTC (or user local timezone ideally, but UTC is simpler)
    response = supabase.table("food_logs").select("*").gte("created_at", f"{today}T00:00:00Z").lte("created_at", f"{today}T23:59:59Z").order("created_at", desc=True).execute()
    return response.data

def delete_food_log(log_id: str):
    if not supabase: return
    supabase.table("food_logs").delete().eq("id", log_id).execute()
