import streamlit as st
st.write("Hello, I am Don!")
s = st.text_input("Enter your name")
if s:
    st.write(f"{s}, nice to meet you!")
