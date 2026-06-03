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

    st.page_link(
        "pages/1_Attendance.py",
        label="Open Attendance System",
        icon="📅"
    )

    st.markdown("""
    <div class="card">
        <h3>📝 Staff Performance Appraisal</h3>
        <p>Analyze employee productivity, conduct staff appraisals, reviews, and assessment processes efficiently.</p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/3_Staff_Performance_Appraisal.py",
        label="Open Staff Performance Appraisal",
        icon="📝"
    )

with right_col:

    st.markdown("""
    <div class="card">
        <h3>💼 Business Department Appraisal</h3>
        <p>Tracks business department productivity, targets, efficiency, and overall departmental performance.</p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/2_Business_Department_Appraisal.py",
        label="Open Business Department Appraisal",
        icon="💼"
    )

    st.markdown("""
    <div class="card">
        <h3>🛠️ Admin Panel</h3>
        <p>Manage high-level administrative tasks, operational setups, and office activities.</p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/4_Admin_Panel.py",
        label="Open Admin Panel",
        icon="🛠️"
    )
