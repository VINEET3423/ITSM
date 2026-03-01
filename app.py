import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("security.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
ip_address TEXT,
status TEXT,
time TEXT
)
""")
conn.commit()

st.title("🚨 Cybersecurity Alert Monitoring")

menu = st.sidebar.selectbox("Menu", ["Log Login", "View Alerts"])

if menu == "Log Login":
    username = st.text_input("Username")
    ip = st.text_input("IP Address")
    status = st.selectbox("Login Status", ["Success", "Failed"])

    if st.button("Log"):
        cursor.execute("""
            INSERT INTO alerts(username,ip_address,status,time)
            VALUES(?,?,?,?)
        """, (username, ip, status, datetime.now()))
        conn.commit()
        st.success("Login Recorded!")

elif menu == "View Alerts":
    df = pd.read_sql_query("SELECT * FROM alerts", conn)
    st.dataframe(df)

    failed = df[df["status"] == "Failed"].shape[0]
    st.metric("Total Failed Attempts", failed)

    if failed > 3:
        st.error("⚠ Multiple Failed Login Attempts Detected!")
