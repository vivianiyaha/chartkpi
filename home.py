import streamlit as st

attendance = st.Page("pages/attendance.py", title="Attendance")
business = st.Page("pages/business.py", title="Business Appraisal")
performance = st.Page("pages/performance.py", title="Performance Appraisal")
admin = st.Page("pages/admin.py", title="Admin Panel")

pg = st.navigation([
    attendance,
    business,
    performance,
    admin
])

pg.run()
