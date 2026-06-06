import streamlit as st

# =========================================
# IMPORT SUB-APPS (STANDARDIZED)
# =========================================
from admin_panel.app import main as admin_app
from attendance.app import main as attendance_app
from business.app import main as business_app
from performance_appraisal.app import main as performance_app

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="HR/Admin Management System",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# SESSION STATE NAVIGATION
# =========================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Hub"


def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()


# =========================================
# CUSTOM CSS (UNCHANGED STYLE)
# =========================================
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }

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

    div.stButton > button {
        background: #ff6b00 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 18px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-bottom: 25px;
    }

    .block-container {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================================
# ROUTING SYSTEM
# =========================================
if st.session_state.current_page != "Dashboard Hub":

    st.markdown("### ⬅ Back to Dashboard")
    if st.button("Return Home"):
        navigate_to("Dashboard Hub")

    st.markdown("---")

    if st.session_state.current_page == "Attendance":
        attendance_app()
        st.stop()

    elif st.session_state.current_page == "Performance":
        performance_app()
        st.stop()

    elif st.session_state.current_page == "Business":
        business_app()
        st.stop()

    elif st.session_state.current_page == "Admin":
        admin_app()
        st.stop()


# =========================================
# DASHBOARD UI
# =========================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("logo.png", width=400)

st.markdown('<div class="main-title">HR/ADMIN MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Smart HR Operations & Employee Analytics Platform</div>', unsafe_allow_html=True)

left_col, right_col = st.columns(2)

with left_col:

    st.markdown("""
    <div class="card">
        <h3>📅 Attendance Management</h3>
        <p>Track employee attendance records, punctuality, daily check-ins.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Attendance System"):
        navigate_to("Attendance")

    st.markdown("""
    <div class="card">
        <h3>📝 Staff Performance Appraisal</h3>
        <p>Analyze employee performance and productivity.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Staff Performance Appraisal"):
        navigate_to("Performance")


with right_col:

    st.markdown("""
    <div class="card">
        <h3>💼 Business Department Appraisal</h3>
        <p>Tracks departmental performance and targets.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Business Department Appraisal"):
        navigate_to("Business")

    st.markdown("""
    <div class="card">
        <h3>🛠️ Admin Panel</h3>
        <p>Manage system settings and operations.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Admin Panel"):
        navigate_to("Admin")
