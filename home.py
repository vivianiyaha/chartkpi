import streamlit as st

st.set_page_config(
    page_title="HR/Admin Management System",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# =========================================
# APPLICATION HUB
# =========================================

left_col, right_col = st.columns(2)

with left_col:

    st.markdown("""
    <div class="card">
        <h3>📅 Attendance Management</h3>
        <p>Track employee attendance records, punctuality, daily check-ins, and workforce presence.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Attendance System"):
        st.switch_page("pages/1_Attendance.py")
    

    st.markdown("""
    <div class="card">
        <h3>📝 Staff Performance Appraisal</h3>
        <p>Analyze employee productivity, conduct staff appraisals, reviews, and assessment processes efficiently.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Performance Appraisal"):
        st.switch_page("pages/3_Performancr_Appraisal.py")
    

with right_col:

    st.markdown("""
    <div class="card">
        <h3>💼 Business Department Appraisal</h3>
        <p>Tracks business department productivity, targets, efficiency, and overall departmental performance.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Business Department Appraisal"):
        st.switch_page("pages/2_Business_Appraisal.py")

    st.markdown("""
    <div class="card">
        <h3>🛠️ Admin Panel</h3>
        <p>Manage high-level administrative tasks, operational setups, and office activities.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Admin Panel"):
        st.switch_page("pages/4_Admin_Panel.py")
