
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px

LESSONS_FILE = Path("Knowledge/Reports/lessons.jsonl")

def load_lessons():
    """Read JSONL file and return DataFrame"""
    if not LESSONS_FILE.exists():
        return pd.DataFrame()

    data = []
    with open(LESSONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    return pd.DataFrame(data)

def render_lessons_trends():
    st.subheader("[INFO] Lessons Learned Trends")
    df = load_lessons()

    if df.empty:
        st.info("No lessons found in lessons.jsonl.")
        return

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- Metrics ---
    col1, col2 = st.columns(2)
    col1.metric("Total Lessons", len(df))
    col2.metric("Critical Insights", len(df[df['impact'] == 'Critical']))

    # --- Charts ---
    st.markdown("### [INFO] Distribution by Category")
    fig_cat = px.pie(df, names='category', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("### [INFO] Insights Over Time")
    df_sorted = df.sort_values('timestamp')
    fig_time = px.line(df_sorted, x='timestamp', y=df_sorted.index, markers=True,
                       labels={'y': 'Cumulative Count'}, title="Knowledge Accumulation")
    st.plotly_chart(fig_time, use_container_width=True)

    # --- Data Table ---
    st.markdown("### [INFO] Raw Insights")
    st.dataframe(df[['timestamp', 'category', 'lesson', 'impact']], use_container_width=True)
