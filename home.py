import streamlit as st

st.set_page_config(
    page_title="HR/Admin Management System",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }

    /* HEADER */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #000000;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 35px;
    }

    /* CARD DESIGN */
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 18px;
        border-left: 6px solid #ff6b00;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        border: 1px solid #f3f4f6;
        transition: 0.3s;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
    }

    .card h3 {
        color: #000000;
        margin-bottom: 10px;
    }

    .card p {
        color: #4b5563;
        line-height: 1.6;
        font-size: 15px;
    }

    /* BUTTONS */
    div.stLinkButton > a {
        background: #ff6b00 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 18px !important;
        font-weight: bold !important;
        text-align: center !important;
        width: 100% !important;
        display: block !important;
        text-decoration: none !important;
        margin-bottom: 30px !important;
    }

    /* REMOVE EXTRA TOP SPACE */
    .block-container {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# LOGO & HEADER
# =========================================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=400)

st.markdown('<div class="main-title">HR/ADMIN MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Smart HR Operations & Employee Analytics Platform</div>', unsafe_allow_html=True)
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
        st.switch_page("pages/Attendance")
    

    st.markdown("""
    <div class="card">
        <h3>📝 Staff Performance Appraisal</h3>
        <p>Analyze employee productivity, conduct staff appraisals, reviews, and assessment processes efficiently.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Performance Appraisal"):
        st.switch_page("pages/Performance-Appraisal")
    

with right_col:

    st.markdown("""
    <div class="card">
        <h3>💼 Business Department Appraisal</h3>
        <p>Tracks business department productivity, targets, efficiency, and overall departmental performance.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Business Department Appraisal"):
        st.switch_page("pages/Business.py")

    st.markdown("""
    <div class="card">
        <h3>🛠️ Admin Panel</h3>
        <p>Manage high-level administrative tasks, operational setups, and office activities.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Admin Panel"):
        st.switch_page("pages/Admin-Panel")
