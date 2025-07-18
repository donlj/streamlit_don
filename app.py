import streamlit as st
import pandas as pd
from datetime import datetime
import re
import os

FILE_NAME = "mental_wellness_entries.xlsx"

def validate_inputs(name, wellness, me_time, screen_time, frequency):
    if not name or not re.match("^[A-Za-z ]+$", name):
        return "Student Name should only contain letters and spaces."
    if not wellness or not re.match("^[A-Za-z ]+$", wellness):
        return "Wellness Activity should only contain letters and spaces."
    if not me_time or not re.match("^[A-Za-z ]+$", me_time):
        return "Me-Time Activity should only contain letters and spaces."
    if not screen_time.isdigit() or int(screen_time) <= 0:
        return "Screen-Free Time must be a positive integer."
    if not frequency or not re.match("^[0-9]+(x| times| per week)?$", frequency):
        return "Frequency should be in format like '3x' or '3 times'."
    return None

def determine_status(screen_time, wellness, me_time):
    return "Healthy" if int(screen_time) >= 60 and wellness and me_time else "Needs More Me-Time"

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME)
    else:
        return pd.DataFrame(columns=["Student Name", "Wellness Activity", "Me-Time Activity", "Screen-Free Time (mins)", "Frequency", "Status", "Timestamp"])

def save_data(df):
    df.to_excel(FILE_NAME, index=False)

st.title("Mental Wellness Logger")

with st.form("entry_form"):
    name = st.text_input("Student Name")
    wellness = st.text_input("Wellness Activity")
    me_time = st.text_input("Me-Time Activity")
    screen_time = st.text_input("Screen-Free Time (mins)")
    frequency = st.text_input("Frequency (e.g., 3x, 2 times)")

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        error = validate_inputs(name, wellness, me_time, screen_time, frequency)
        if error:
            st.error(error)
        else:
            status = determine_status(screen_time, wellness, me_time)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([[name, wellness, me_time, int(screen_time), frequency, status, timestamp]],
                                    columns=["Student Name", "Wellness Activity", "Me-Time Activity", "Screen-Free Time (mins)", "Frequency", "Status", "Timestamp"])
            df = load_data()
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("Entry added successfully!")

st.header("All Entries")
df = load_data()
st.dataframe(df)

if st.button("Clear All Entries"):
    save_data(pd.DataFrame(columns=df.columns))
    st.success("All entries cleared!")

st.header("Statistics")
healthy_count = df[df["Status"] == "Healthy"].shape[0]
needs_more_count = df[df["Status"] == "Needs More Me-Time"].shape[0]
st.write(f"Total Entries: {df.shape[0]}")
st.write(f"Healthy: {healthy_count}")
st.write(f"Needs More Me-Time: {needs_more_count}")
