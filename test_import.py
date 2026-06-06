import streamlit as st

# =========================================
# IMPORT SUB-APP FUNCTIONS
# =========================================
# Adjust the import paths/filenames if your inner entry scripts use different names
from admin_panel.app import run_admin_panel
from attendance.app import run_attendance
from business.app import run_business
from performance_appraisal.app import run_performance

# =========================================
# INITIALIZE GLOBAL PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="HR/Admin Management System",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize navigation state tracking
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Hub"

# Function to handle app navigation cleanly
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# =========================================
# CUSTOM GLOBAL CSS
# =========================================
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }

    /* HEADER STYLING */
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

    /* HUB CARD DESIGN */
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

    /* HUB STYLE BUTTONS */
    div.stButton > button {
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
        transition: 0.2s ease-in-out;
    }
    
    div.stButton > button:hover {
        background: #e05e00 !important;
        color: white !important;
    }

    /* TOP BAR BACK BUTTON STYLING */
    div.back-btn-container > div > div > button {
        background: #374151 !important; /* Charcoal Gray */
        margin-bottom: 15px !important;
        width: auto !important;
    }

    .block-container {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================================
# ROUTER LOGIC
# =========================================

# --- CASE 1: MAIN HUB DASHBOARD ---
if st.session_state.current_page == "Dashboard Hub":
    
    # Header Layout
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            st.image("logo.png", width=400)
        except:
            st.warning("Logo image file not found. Ensure 'logo.png' is in the root directory.")

    st.markdown('<div class="main-title">HR/ADMIN MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Smart HR Operations & Employee Analytics Platform</div>', unsafe_allow_html=True)

    # Content Grid
    left_col, right_col = st.columns(2)

    with left_col:
        # Card 1: Attendance
        st.markdown("""
        <div class="card">
            <h3>📅 Attendance Management</h3>
            <p>Track employee attendance records, punctuality, daily check-ins, and workforce presence.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Attendance System", key="btn_attendance"):
            navigate_to("Attendance")

        # Card 2: Staff Performance
        st.markdown("""
        <div class="card">
            <h3>📝 Staff Performance Appraisal</h3>
            <p>Analyze employee productivity, conduct staff appraisals, reviews, and assessment processes efficiently.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Staff Performance Appraisal", key="btn_performance"):
            navigate_to("Staff Performance")

    with right_col:
        # Card 3: Business Department
        st.markdown("""
        <div class="card">
            <h3>💼 Business Department Appraisal</h3>
            <p>Tracks business department productivity, targets, efficiency, and overall departmental performance.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Business Department Appraisal", key="btn_business"):
            navigate_to("Business Department")

        # Card 4: Admin Panel
        st.markdown("""
        <div class="card">
            <h3>🛠️ Admin Panel</h3>
            <p>Manage high-level administrative tasks, operational setups, and office activities.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Admin Panel", key="btn_admin"):
            navigate_to("Admin Panel")


# --- CASE 2: EXECUTE INDIVIDUAL SUB-APPS ---
else:
    # Render a universal "Return to Main Menu" control bar above the active sub-app layout
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    if st.button("⬅ Back to Dashboard Menu", key="global_back_btn"):
        navigate_to("Dashboard Hub")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Route and mount the targeted interface module conditionally
    if st.session_state.current_page == "Attendance":
        run_attendance()
        
    elif st.session_state.current_page == "Staff Performance":
        run_performance()
        
    elif st.session_state.current_page == "Business Department":
        run_business()
        
    elif st.session_state.current_page == "Admin Panel":
        run_admin_panel()
