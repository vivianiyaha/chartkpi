import streamlit as st

st.set_page_config(
    page_title="HR/Admin Management System",
    page_icon="logo.png",
    layout="wide"
)

st.image("logo.png", width=350)

st.title("HR/ADMIN MANAGEMENT SYSTEM")

st.markdown("""
### Welcome

Use the sidebar to access:

- Attendance Management
- Business Department Appraisal
- Staff Performance Appraisal
- Admin Panel
""")
