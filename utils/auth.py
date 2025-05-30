# utils/auth.py
import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client

def get_client():
    sb = st.connection(
        "supabase",
        type=SupabaseConnection,
        url="https://jlbiqjoqubduikjvwsed.supabase.co",
        key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsYmlxam9xdWJkdWlranZ3c2VkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwMTQ0NTcsImV4cCI6MjA2MzU5MDQ1N30.IWmUnEobN4A_vWBZkImJVf3TUpyhCGgCOSYNvCOGgjg"
    )   
    return sb.client                     

def get_admin_client_direct():
    url = "https://jlbiqjoqubduikjvwsed.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsYmlxam9xdWJkdWlranZ3c2VkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwMTQ0NTcsImV4cCI6MjA2MzU5MDQ1N30.IWmUnEobN4A_vWBZkImJVf3TUpyhCGgCOSYNvCOGgjg"
    return create_client(url, key)

def get_user():
    return st.session_state.get("user")

def require_login():
    user = st.session_state.get("user")

    if not user: 
        st.error("로그인 후 이용 가능합니다.")
        st.page_link("pages/login.py", label="👉 로그인하기")
        st.stop()
    return user
    