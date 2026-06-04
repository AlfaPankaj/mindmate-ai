import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="MindMate AI Companion", layout="wide")

API_BASE = "http://localhost:8000"
USER_ID = "demo_user_001"

st.title("🧠 MindMate AI: Mental Health Companion")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Demo Controls")
    if st.button("Trigger Daily Check-in"):
        st.info("Triggering proactive evaluation...")
        try:
            response = requests.post(
                f"{API_BASE}/chat", 
                json={"user_id": USER_ID, "message": "[DAILY_CHECKIN_TRIGGER]"},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append({"role": "assistant", "content": data["response"]})
                st.rerun()
            else:
                st.error(f"Backend returned error: {response.status_code}")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The AI might be taking too long to reason.")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat History")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

with col2:
    st.subheader("Module Dashboard")
    
    try:
        profile_res = requests.get(f"{API_BASE}/profile/{USER_ID}").json()
        habits_res = requests.get(f"{API_BASE}/habits/{USER_ID}").json()
        moods_res = requests.get(f"{API_BASE}/moods/{USER_ID}").json()
        
        st.markdown("### 🔍 Detected Patterns")
        patterns = profile_res.get("active_patterns", {})
        if patterns:
            for p_name, p_data in patterns.items():
                st.info(f"**{p_name}**\n\nEvidence Count: {p_data.get('evidence_count', 0)}")
        else:
            st.write("No patterns detected yet.")

        st.markdown("### 🏃 Habit Tracking")
        if habits_res and not isinstance(habits_res, dict): 
            df_habits = pd.DataFrame(habits_res)
            st.table(df_habits[['name', 'status', 'streak']])
        else:
            st.write("No active habits.")

        st.markdown("### 📊 Mood History")
        if moods_res and not isinstance(moods_res, dict):
            df_moods = pd.DataFrame(moods_res)
            if not df_moods.empty:
                df_moods['timestamp'] = pd.to_datetime(df_moods['timestamp'])
                df_moods = df_moods.sort_values('timestamp')
                
                df_moods['time_display'] = df_moods['timestamp'].dt.strftime('%m/%d %H:%M')
                
                st.bar_chart(df_moods.set_index('time_display')['score'])
        else:
            st.write("No mood logs yet.")
            
    except Exception as e:
        st.warning("Dashboard data offline.")

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    try:
        response = requests.post(
            f"{API_BASE}/chat", 
            json={"user_id": USER_ID, "message": prompt},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            full_response = data["response"]
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun() 
        else:
            st.error(f"Backend returned error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("Request timed out. The AI is taking longer than 30 seconds to respond.")
    except Exception as e:
        st.error(f"Backend unreachable: {str(e)}")

st.markdown("---")
st.caption("MindMate AI Prototype - Built with LangGraph, FastAPI, and LLaMA 3.3.")
