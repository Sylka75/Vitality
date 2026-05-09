import streamlit as st
from database import get_user_profile, get_today_food_logs, insert_food_log, delete_food_log, update_weight, update_goal_calories, get_weight_history
from ai_services import describe_image, parse_food_description
from PIL import Image
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vitality - Personal Calorie Tracker",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLE SYSTEM (UI/UX Pro Max) ---
# Primary: #10B981 (Emerald), Background: #F8FAFC, Text: #1E293B
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

    :root {
        --primary: #10B981;
        --primary-soft: #ECFDF5;
        --secondary: #3B82F6;
        --bg: #F8FAFC;
        --card-bg: #FFFFFF;
        --text: #1E293B;
        --text-muted: #64748B;
        --border: #E2E8F0;
        --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        --shadow-hover: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }

    html, body, [class*="st-"] {
        font-family: 'Open Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
    }

    h1, h2, h3, .stHeader {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: var(--text);
    }

    /* Bento Card Styling */
    .bento-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .bento-card:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    /* Stat Highlight */
    .stat-val {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
        margin-bottom: 0.25rem;
    }

    .stat-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Progress Bar */
    .progress-container {
        background: var(--border);
        border-radius: 999px;
        height: 12px;
        width: 100%;
        margin-top: 1rem;
        overflow: hidden;
    }

    .progress-fill {
        background: var(--primary);
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease;
    }

    /* Custom Button */
    .stButton>button {
        border-radius: 0.5rem;
        border: none;
        background: var(--primary);
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: #059669;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Content Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA FETCHING ---
profile = get_user_profile()
logs = get_today_food_logs()
weight_hist = get_weight_history()

if not profile:
    st.error("Profile not found. Database might not be initialized.")
    st.stop()

# --- APP LOGIC ---
total_calories = sum(log['calories'] for log in logs)
goal = profile['goal_calories']
remaining = max(0, goal - total_calories)
pct = min(100, (total_calories / goal) * 100) if goal > 0 else 0

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown(f"<h1>Hello, Vitality 🌿</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: var(--text-muted); font-size: 1.1rem;'>Track your energy, fuel your potential.</p>", unsafe_allow_html=True)

with col_h2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    if st.button("⚙️ Settings"):
        st.session_state.show_settings = not st.get('show_settings', False)
    st.markdown("</div>", unsafe_allow_html=True)

# --- DASHBOARD (BENTO GRID) ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(f"""
        <div class="bento-card">
            <div class="stat-label">Consumed</div>
            <div class="stat-val">{total_calories}</div>
            <div class="stat-label">kcal today</div>
            <div class="progress-container">
                <div class="progress-fill" style="width: {pct}%"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="bento-card">
            <div class="stat-label">Remaining</div>
            <div class="stat-val">{remaining}</div>
            <div class="stat-label">kcal to goal</div>
            <div style="margin-top: 1.5rem; font-size: 0.9rem; color: var(--text-muted);">
                Goal: <b>{goal} kcal</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    current_weight = profile['current_weight'] or "N/A"
    st.markdown(f"""
        <div class="bento-card">
            <div class="stat-label">Weight</div>
            <div class="stat-val">{current_weight} <span style="font-size: 1.2rem;">kg</span></div>
            <div class="stat-label">Current status</div>
            <div style="margin-top: 1.5rem;">
                <span style="background: var(--primary-soft); color: var(--primary); padding: 4px 12px; border-radius: 99px; font-size: 0.8rem; font-weight: 600;">STABLE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN ACTIONS & LOGS ---
m_col1, m_col2 = st.columns([1, 1])

with m_col1:
    st.markdown("<h3>Log Your Food</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        img_file = st.file_uploader("Capture or upload a meal image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if img_file:
            image = Image.open(img_file)
            st.image(image, use_container_width=True, caption="Meal captured")
            
            if st.button("Analyze with AI ✨", use_container_width=True):
                with st.spinner("AI is examining your meal..."):
                    description = describe_image(image)
                    if "Error" in description:
                        st.error(description)
                    else:
                        analysis = parse_food_description(description)
                        if "error" in analysis:
                            st.error(analysis["error"])
                        else:
                            st.success(f"Identified: {analysis['label']} ({analysis['calories']} kcal)")
                            st.session_state.pending_log = analysis

        if "pending_log" in st.session_state:
            pending = st.session_state.pending_log
            st.markdown(f"**Confirm Log:** {pending['emoji']} {pending['label']} - {pending['calories']} kcal")
            if st.button("Save to Log", key="save_log"):
                insert_food_log(pending['label'], pending['calories'], pending['emoji'], pending)
                st.toast("Food logged successfully!", icon="✅")
                del st.session_state.pending_log
                st.rerun()

    st.markdown("<br><h3>Weight Tracking</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        new_w = st.number_input("Update Current Weight (kg)", value=float(profile['current_weight'] or 70.0), step=0.1)
        if st.button("Update Weight"):
            update_weight(new_w)
            st.toast("Weight updated!")
            st.rerun()

with m_col2:
    st.markdown("<h3>Today's Energy</h3>", unsafe_allow_html=True)
    if not logs:
        st.info("No food logged yet. Start by capturing a meal!")
    else:
        for log in logs:
            col_l1, col_l2, col_l3 = st.columns([0.15, 0.65, 0.2])
            with col_l1:
                st.markdown(f"<div style='font-size: 1.5rem;'>{log['emoji']}</div>", unsafe_allow_html=True)
            with col_l2:
                st.markdown(f"<b>{log['label']}</b><br><span style='color: var(--text-muted); font-size: 0.85rem;'>{log['calories']} kcal</span>", unsafe_allow_html=True)
            with col_l3:
                if st.button("🗑️", key=f"del_{log['id']}"):
                    delete_food_log(log['id'])
                    st.rerun()
            st.divider()

# --- ANALYTICS ---
if weight_hist:
    st.markdown("<br><h3>Trends</h3>", unsafe_allow_html=True)
    df_weight = pd.DataFrame(weight_hist)
    df_weight['recorded_at'] = pd.to_datetime(df_weight['recorded_at'])
    fig = px.line(df_weight, x='recorded_at', y='weight_value', 
                  labels={'weight_value': 'Weight (kg)', 'recorded_at': 'Date'},
                  template="plotly_white",
                  markers=True)
    fig.update_traces(line_color='#10B981')
    fig.update_layout(
        font_family="Open Sans",
        title_font_family="Poppins",
        margin=dict(l=0, r=0, t=30, b=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SETTINGS OVERLAY ---
if st.session_state.get('show_settings', False):
    with st.sidebar:
        st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
        new_goal = st.number_input("Daily Calorie Goal", value=int(profile['goal_calories']), step=50)
        if st.button("Save Settings"):
            update_goal_calories(new_goal)
            st.session_state.show_settings = False
            st.rerun()
