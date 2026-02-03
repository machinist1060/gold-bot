import streamlit as st
import os

st.title("Gold Market Intelligence Bot")
st.caption("Updated daily with live data")

report_path = os.path.join(os.path.dirname(__file__), "../reports/daily_gold_report.md")

if os.path.exists(report_path):
    with open(report_path, "r") as f:
        st.markdown(f.read())
else:
    st.write("Daily report not yet generated.")
