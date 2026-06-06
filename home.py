import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from io import BytesIO
from datetime import date, datetime, timedelta

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="HR/Admin Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp { background-color: #f8f9fa; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] .stRadio label {
        color: #cccccc !important;
        font-size: 15px;
        padding: 6px 0;
    }
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
        font-size: 13px !important;
        color: #aaaaaa !important;
    }

    /* Remove red lines from sidebar radio */
    [data-testid="stSidebar"] .stRadio > div { gap: 4px; }

    /* Main area */
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Page title */
    .page-header {
        background: linear-gradient(135deg, #ff6b00 0%, #ff8c00 100%);
        color: white;
        padding: 20px 28px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(255,107,0,0.3);
    }
    .page-header h1 { margin: 0; font-size: 26px; font-weight: 800; }
    .page-header p  { margin: 4px 0 0; font-size: 14px; opacity: 0.85; }

    /* Cards */
    .card {
        background: #ffffff;
        padding: 22px;
        border-radius: 14px;
        border-left: 5px solid #ff6b00;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        margin-bottom: 16px;
    }
    .card h3 { margin: 0 0 8px; font-size: 17px; color: #111; }
    .card p  { margin: 0; font-size: 14px; color: #555; line-height: 1.6; }

    /* Metric cards */
    .metric-box {
        background: #fff;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        text-align: center;
        border-top: 4px solid #ff6b00;
    }
    .metric-box .val { font-size: 32px; font-weight: 800; color: #ff6b00; }
    .metric-box .lbl { font-size: 13px; color: #666; margin-top: 4px; }

    /* Tables */
    .dataframe thead th {
        background-color: #ff6b00 !important;
        color: white !important;
    }

    /* Orange buttons */
    .stButton > button {
        background: #ff6b00 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;
    }
    .stButton > button:hover {
        background: #e05a00 !important;
        box-shadow: 0 4px 12px rgba(255,107,0,0.35) !important;
    }

    /* Section heading */
    .sec-head {
        font-size: 18px;
        font-weight: 700;
        color: #1a1a1a;
        border-bottom: 3px solid #ff6b00;
        padding-bottom: 6px;
        margin: 24px 0 16px;
    }

    /* Status badges */
    .badge-present  { background:#dcfce7; color:#166534; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-absent   { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-late     { background:#fef9c3; color:#854d0e; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-leave    { background:#e0e7ff; color:#3730a3; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }

    /* Hide streamlit branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR NAVIGATION
# =========================================
with st.sidebar:
    st.markdown("### 🏢 HR/Admin System")
    st.markdown("---")
    page = st.radio(
        "Navigate to",
        [
            "🏠 Home",
            "📅 Attendance Management",
            "💼 Business Department Appraisal",
            "📝 Staff Performance Appraisal",
            "🛠️ Admin Panel",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("<small style='color:#888'>Cardstel Solutions Limited</small>", unsafe_allow_html=True)

# =========================================
# HELPERS
# =========================================
def page_header(title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {'<p>'+subtitle+'</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="sec-head">{title}</div>', unsafe_allow_html=True)

def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="val">{value}</div>
                <div class="lbl">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# =========================================
# FILE / DATA HELPERS
# =========================================
ATTENDANCE_DIR = Path("daily-attendance")
LEAVE_DIR      = Path("leave-management")
EMPLOYEE_FILE  = Path("employee.csv")

def ensure_dirs():
    ATTENDANCE_DIR.mkdir(exist_ok=True)
    LEAVE_DIR.mkdir(exist_ok=True)
    if not EMPLOYEE_FILE.exists():
        pd.DataFrame({"Name": [], "Department": [], "Position": [], "Email": [], "Phone": []}).to_csv(EMPLOYEE_FILE, index=False)

def load_employees():
    ensure_dirs()
    if EMPLOYEE_FILE.exists():
        df = pd.read_csv(EMPLOYEE_FILE)
        if df.empty or "Name" not in df.columns:
            return pd.DataFrame({"Name": [], "Department": [], "Position": [], "Email": [], "Phone": []})
        return df
    return pd.DataFrame({"Name": [], "Department": [], "Position": [], "Email": [], "Phone": []})

def save_employees(df):
    ensure_dirs()
    df.to_csv(EMPLOYEE_FILE, index=False)

def load_attendance(day: date):
    path = ATTENDANCE_DIR / f"{day.strftime('%B %-d, %Y')}.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame({"Name": [], "Status": [], "Time In": [], "Time Out": [], "Notes": []})

def save_attendance(df, day: date):
    path = ATTENDANCE_DIR / f"{day.strftime('%B %-d, %Y')}.csv"
    df.to_csv(path, index=False)

def load_leave(month_name: str):
    path = LEAVE_DIR / f"{month_name}.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame({"Name": [], "Leave Type": [], "Start Date": [], "End Date": [], "Days": [], "Status": [], "Reason": []})

def save_leave(df, month_name: str):
    path = LEAVE_DIR / f"{month_name}.csv"
    df.to_csv(path, index=False)

# =========================================
# BUSINESS DEPT DATA HELPER
# =========================================
BUSINESS_DIR = Path("business-data")
def ensure_business():
    BUSINESS_DIR.mkdir(exist_ok=True)

def load_business(month: str):
    ensure_business()
    path = BUSINESS_DIR / f"{month}.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame({
        "Department": [], "Target (₦)": [], "Achieved (₦)": [],
        "Efficiency (%)": [], "Staff Count": [], "Notes": []
    })

def save_business(df, month: str):
    ensure_business()
    path = BUSINESS_DIR / f"{month}.csv"
    df.to_csv(path, index=False)

# =========================================
# STAFF PERFORMANCE DATA HELPER
# =========================================
PERF_DIR = Path("performance-reports")
def ensure_perf():
    PERF_DIR.mkdir(exist_ok=True)

def load_perf(month: str):
    ensure_perf()
    path = PERF_DIR / f"{month}.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame({
        "Name": [], "Department": [], "KPI Score": [], "Attendance Score": [],
        "Teamwork Score": [], "Productivity Score": [], "Overall (%)": [], "Grade": [], "Comments": []
    })

def save_perf(df, month: str):
    ensure_perf()
    path = PERF_DIR / f"{month}.csv"
    df.to_csv(path, index=False)

# =========================================
# ADMIN DATA HELPERS
# =========================================
ADMIN_DIR    = Path("Consumables_Records")
MEETINGS_DIR = Path("Meetings")
REPORTS_DIR  = Path("Reports")
STOCK_DIR    = Path("Stock_Records")

def ensure_admin():
    for d in [ADMIN_DIR, MEETINGS_DIR, REPORTS_DIR, STOCK_DIR]:
        d.mkdir(exist_ok=True)

def load_csv_admin(path):
    if Path(path).exists():
        return pd.read_csv(path)
    return pd.DataFrame()

def save_csv_admin(df, path):
    df.to_csv(path, index=False)

# =========================================
# PAGE: HOME
# =========================================
def show_home():
    try:
        if os.path.exists("logo.png"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("logo.png", width=350)
    except Exception:
        pass

    st.markdown('<div class="main-title" style="font-size:36px;font-weight:800;text-align:center;color:#000;margin:10px 0 5px;">HR/ADMIN MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#6b7280;font-size:17px;margin-bottom:30px;">Smart HR Operations & Employee Analytics Platform</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    modules = [
        ("📅 Attendance Management",
         "Track employee attendance records, punctuality, daily check-ins, and workforce presence.",
         "📅 Attendance Management"),
        ("💼 Business Department Appraisal",
         "Tracks business department productivity, targets, efficiency, and overall departmental performance.",
         "💼 Business Department Appraisal"),
        ("📝 Staff Performance Appraisal",
         "Analyze employee productivity, conduct staff appraisals, reviews, and assessment processes efficiently.",
         "📝 Staff Performance Appraisal"),
        ("🛠️ Admin Panel",
         "Manage high-level administrative tasks, operational setups, and office activities.",
         "🛠️ Admin Panel"),
    ]
    for i, (title, desc, nav_key) in enumerate(modules):
        col = left if i % 2 == 0 else right
        with col:
            st.markdown(f"""
            <div class="card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {title.split(' ', 1)[1]}", key=f"home_btn_{i}"):
                st.session_state["_nav_target"] = nav_key
                st.rerun()

# =========================================
# PAGE: ATTENDANCE MANAGEMENT
# =========================================
def show_attendance():
    page_header("📅 Attendance Management", "Track daily attendance, leaves, and employee check-ins")
    ensure_dirs()

    tabs = st.tabs(["📋 Daily Attendance", "🗓️ Leave Management", "👥 Employee Register", "📊 Reports"])

    # ---- TAB 1: Daily Attendance ----
    with tabs[0]:
        section("Record Daily Attendance")
        col1, col2 = st.columns([1, 3])
        with col1:
            sel_date = st.date_input("Select Date", value=date.today(), key="att_date")

        emp_df = load_employees()
        att_df = load_attendance(sel_date)

        if emp_df.empty or "Name" not in emp_df.columns or emp_df["Name"].dropna().empty:
            st.info("No employees registered yet. Add employees in the **Employee Register** tab.")
        else:
            emp_names = emp_df["Name"].dropna().tolist()
            existing_names = att_df["Name"].tolist() if not att_df.empty else []

            # Build attendance form
            statuses, times_in, times_out, notes_list = [], [], [], []

            with st.form("attendance_form"):
                st.markdown(f"**Date: {sel_date.strftime('%A, %B %d, %Y')}**")
                header_cols = st.columns([3, 2, 2, 2, 3])
                header_cols[0].markdown("**Employee**")
                header_cols[1].markdown("**Status**")
                header_cols[2].markdown("**Time In**")
                header_cols[3].markdown("**Time Out**")
                header_cols[4].markdown("**Notes**")

                row_data = []
                for name in emp_names:
                    existing_row = att_df[att_df["Name"] == name] if not att_df.empty else pd.DataFrame()
                    def_status = existing_row["Status"].values[0] if not existing_row.empty else "Present"
                    def_tin    = existing_row["Time In"].values[0] if not existing_row.empty and "Time In" in existing_row else "08:00"
                    def_tout   = existing_row["Time Out"].values[0] if not existing_row.empty and "Time Out" in existing_row else "17:00"
                    def_notes  = existing_row["Notes"].values[0] if not existing_row.empty and "Notes" in existing_row else ""

                    r = st.columns([3, 2, 2, 2, 3])
                    r[0].markdown(f"**{name}**")
                    status  = r[1].selectbox("", ["Present", "Absent", "Late", "On Leave", "Half Day"],
                                             index=["Present","Absent","Late","On Leave","Half Day"].index(def_status)
                                             if def_status in ["Present","Absent","Late","On Leave","Half Day"] else 0,
                                             key=f"status_{name}", label_visibility="collapsed")
                    time_in  = r[2].text_input("", value=str(def_tin) if pd.notna(def_tin) else "08:00",
                                               key=f"tin_{name}", label_visibility="collapsed")
                    time_out = r[3].text_input("", value=str(def_tout) if pd.notna(def_tout) else "17:00",
                                               key=f"tout_{name}", label_visibility="collapsed")
                    note     = r[4].text_input("", value=str(def_notes) if pd.notna(def_notes) else "",
                                               key=f"note_{name}", label_visibility="collapsed")
                    row_data.append({"Name": name, "Status": status, "Time In": time_in,
                                     "Time Out": time_out, "Notes": note})

                if st.form_submit_button("💾 Save Attendance", use_container_width=True):
                    new_df = pd.DataFrame(row_data)
                    save_attendance(new_df, sel_date)
                    st.success(f"✅ Attendance saved for {sel_date.strftime('%B %d, %Y')}!")
                    st.rerun()

        # Show saved
        saved = load_attendance(sel_date)
        if not saved.empty:
            section("Today's Summary")
            present = len(saved[saved["Status"] == "Present"])
            absent  = len(saved[saved["Status"] == "Absent"])
            late    = len(saved[saved["Status"] == "Late"])
            leave   = len(saved[saved["Status"] == "On Leave"])
            metric_row([
                ("Present", present), ("Absent", absent),
                ("Late", late), ("On Leave", leave)
            ])
            st.dataframe(saved, use_container_width=True)

    # ---- TAB 2: Leave Management ----
    with tabs[1]:
        section("Leave Requests")
        months = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"]
        sel_month = st.selectbox("Select Month", months,
                                 index=date.today().month - 1, key="leave_month")
        leave_df = load_leave(sel_month)
        emp_df   = load_employees()

        with st.expander("➕ Add New Leave Request"):
            with st.form("leave_form"):
                c1, c2 = st.columns(2)
                emp_list = emp_df["Name"].dropna().tolist() if not emp_df.empty else []
                leave_name  = c1.selectbox("Employee", emp_list if emp_list else ["—"])
                leave_type  = c2.selectbox("Leave Type", ["Annual Leave","Sick Leave","Maternity Leave","Paternity Leave","Emergency Leave","Unpaid Leave"])
                c3, c4 = st.columns(2)
                start_d = c3.date_input("Start Date", key="leave_start")
                end_d   = c4.date_input("End Date",   key="leave_end")
                reason  = st.text_area("Reason")
                status  = st.selectbox("Status", ["Pending","Approved","Rejected"])
                if st.form_submit_button("Submit Leave Request"):
                    days = (end_d - start_d).days + 1
                    new_row = pd.DataFrame([{
                        "Name": leave_name, "Leave Type": leave_type,
                        "Start Date": str(start_d), "End Date": str(end_d),
                        "Days": days, "Status": status, "Reason": reason
                    }])
                    leave_df = pd.concat([leave_df, new_row], ignore_index=True)
                    save_leave(leave_df, sel_month)
                    st.success("Leave request submitted!")
                    st.rerun()

        if not leave_df.empty:
            st.dataframe(leave_df, use_container_width=True)

            # Allow status update
            section("Update Leave Status")
            with st.form("leave_update"):
                idx = st.selectbox("Select Row (index)", leave_df.index.tolist())
                new_status = st.selectbox("New Status", ["Pending","Approved","Rejected"])
                if st.form_submit_button("Update"):
                    leave_df.at[idx, "Status"] = new_status
                    save_leave(leave_df, sel_month)
                    st.success("Updated!")
                    st.rerun()
        else:
            st.info("No leave records for this month.")

    # ---- TAB 3: Employee Register ----
    with tabs[2]:
        section("Employee Register")
        emp_df = load_employees()

        with st.expander("➕ Add New Employee"):
            with st.form("emp_form"):
                c1, c2 = st.columns(2)
                name   = c1.text_input("Full Name")
                dept   = c2.text_input("Department")
                c3, c4 = st.columns(2)
                pos    = c3.text_input("Position")
                email  = c4.text_input("Email")
                phone  = st.text_input("Phone")
                if st.form_submit_button("Add Employee"):
                    if name:
                        new_emp = pd.DataFrame([{"Name": name, "Department": dept,
                                                  "Position": pos, "Email": email, "Phone": phone}])
                        emp_df = pd.concat([emp_df, new_emp], ignore_index=True)
                        save_employees(emp_df)
                        st.success(f"Employee '{name}' added!")
                        st.rerun()
                    else:
                        st.warning("Name is required.")

        if not emp_df.empty:
            st.dataframe(emp_df, use_container_width=True)
            metric_row([("Total Employees", len(emp_df))])

            # Remove employee
            with st.expander("🗑️ Remove Employee"):
                del_name = st.selectbox("Select Employee to Remove", emp_df["Name"].tolist())
                if st.button("Remove", key="del_emp"):
                    emp_df = emp_df[emp_df["Name"] != del_name]
                    save_employees(emp_df)
                    st.success(f"'{del_name}' removed.")
                    st.rerun()
        else:
            st.info("No employees registered yet.")

    # ---- TAB 4: Reports ----
    with tabs[3]:
        section("Attendance Reports")
        months = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"]
        report_month = st.selectbox("Select Month for Report", months,
                                    index=date.today().month - 1, key="att_report_month")

        # Collect all attendance files for the month
        all_files = list(ATTENDANCE_DIR.glob("*.csv"))
        month_files = [f for f in all_files if report_month in f.name]

        if month_files:
            all_records = []
            for f in sorted(month_files):
                df_tmp = pd.read_csv(f)
                day_str = f.stem
                df_tmp.insert(0, "Date", day_str)
                all_records.append(df_tmp)
            combined = pd.concat(all_records, ignore_index=True)
            st.dataframe(combined, use_container_width=True)

            if "Status" in combined.columns:
                summary = combined["Status"].value_counts().reset_index()
                summary.columns = ["Status", "Count"]
                metric_row([(row["Status"], row["Count"]) for _, row in summary.iterrows()])

            # Download
            csv_bytes = combined.to_csv(index=False).encode()
            st.download_button("⬇️ Download Report", csv_bytes,
                               f"Attendance_{report_month}.csv", "text/csv")
        else:
            st.info(f"No attendance records found for {report_month}.")


# =========================================
# PAGE: BUSINESS DEPARTMENT APPRAISAL
# =========================================
def show_business():
    page_header("💼 Business Department Appraisal",
                "Track departmental productivity, targets, and efficiency")
    ensure_business()

    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

    tabs = st.tabs(["📊 Enter / View Data", "📈 Analytics", "📁 All Records"])

    with tabs[0]:
        sel_month = st.selectbox("Select Month", months,
                                 index=date.today().month - 1, key="biz_month")
        biz_df = load_business(sel_month)

        section("Add / Update Department Record")
        with st.form("biz_form"):
            c1, c2 = st.columns(2)
            dept   = c1.text_input("Department Name")
            target = c2.number_input("Monthly Target (₦)", min_value=0, step=100000)
            c3, c4 = st.columns(2)
            achieved = c3.number_input("Amount Achieved (₦)", min_value=0, step=100000)
            staff    = c4.number_input("Staff Count", min_value=0, step=1)
            notes = st.text_area("Notes / Comments")

            if st.form_submit_button("💾 Save Record"):
                if dept:
                    efficiency = round((achieved / target * 100), 1) if target > 0 else 0
                    new_row = pd.DataFrame([{
                        "Department": dept, "Target (₦)": target,
                        "Achieved (₦)": achieved, "Efficiency (%)": efficiency,
                        "Staff Count": staff, "Notes": notes
                    }])
                    # Update if exists
                    if not biz_df.empty and dept in biz_df["Department"].values:
                        biz_df.loc[biz_df["Department"] == dept] = new_row.values
                    else:
                        biz_df = pd.concat([biz_df, new_row], ignore_index=True)
                    save_business(biz_df, sel_month)
                    st.success("Record saved!")
                    st.rerun()
                else:
                    st.warning("Department name is required.")

        if not biz_df.empty:
            section(f"{sel_month} — Department Records")
            st.dataframe(biz_df, use_container_width=True)

            total_target   = biz_df["Target (₦)"].sum() if "Target (₦)" in biz_df else 0
            total_achieved = biz_df["Achieved (₦)"].sum() if "Achieved (₦)" in biz_df else 0
            avg_eff        = biz_df["Efficiency (%)"].mean() if "Efficiency (%)" in biz_df else 0
            metric_row([
                ("Total Target (₦)", f"{total_target:,.0f}"),
                ("Total Achieved (₦)", f"{total_achieved:,.0f}"),
                ("Avg Efficiency", f"{avg_eff:.1f}%"),
                ("Departments", len(biz_df))
            ])
        else:
            st.info("No records for this month yet.")

    with tabs[1]:
        sel_month2 = st.selectbox("Select Month", months,
                                   index=date.today().month - 1, key="biz_month2")
        biz_df2 = load_business(sel_month2)
        if not biz_df2.empty and "Efficiency (%)" in biz_df2.columns:
            try:
                import plotly.express as px
                fig = px.bar(biz_df2, x="Department", y=["Target (₦)", "Achieved (₦)"],
                             barmode="group", title=f"Target vs Achieved — {sel_month2}",
                             color_discrete_sequence=["#ff6b00", "#1a1a1a"])
                fig.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff")
                st.plotly_chart(fig, use_container_width=True)

                fig2 = px.bar(biz_df2, x="Department", y="Efficiency (%)",
                              title="Efficiency by Department",
                              color="Efficiency (%)",
                              color_continuous_scale=["#fee2e2","#ff6b00","#166534"])
                st.plotly_chart(fig2, use_container_width=True)
            except ImportError:
                st.dataframe(biz_df2[["Department","Efficiency (%)"]], use_container_width=True)
        else:
            st.info("No data to visualise for this month.")

    with tabs[2]:
        section("All Monthly Records")
        all_biz = list(BUSINESS_DIR.glob("*.csv")) if BUSINESS_DIR.exists() else []
        if all_biz:
            combined = pd.concat([pd.read_csv(f).assign(Month=f.stem) for f in sorted(all_biz)], ignore_index=True)
            st.dataframe(combined, use_container_width=True)
            csv_bytes = combined.to_csv(index=False).encode()
            st.download_button("⬇️ Download All Records", csv_bytes, "Business_Dept_All.csv", "text/csv")
        else:
            st.info("No records found yet.")


# =========================================
# PAGE: STAFF PERFORMANCE APPRAISAL
# =========================================
def show_performance():
    page_header("📝 Staff Performance Appraisal",
                "Evaluate employee productivity, KPIs, and overall performance")
    ensure_perf()
    ensure_dirs()

    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

    tabs = st.tabs(["📝 Appraisal Entry", "📊 Analytics", "📁 All Reports"])

    def grade(score):
        if score >= 90: return "A+"
        elif score >= 80: return "A"
        elif score >= 70: return "B"
        elif score >= 60: return "C"
        elif score >= 50: return "D"
        else: return "F"

    with tabs[0]:
        sel_month = st.selectbox("Select Month", months,
                                 index=date.today().month - 1, key="perf_month")
        perf_df = load_perf(sel_month)
        emp_df  = load_employees()

        section("Add Appraisal Record")
        with st.form("perf_form"):
            emp_list = emp_df["Name"].dropna().tolist() if not emp_df.empty else []
            c1, c2 = st.columns(2)
            name = c1.selectbox("Employee", emp_list if emp_list else ["—"])
            dept = c2.text_input("Department")

            st.markdown("**Scores (0 – 100)**")
            c3, c4, c5, c6 = st.columns(4)
            kpi_score   = c3.number_input("KPI Score",         0, 100, 75, key="kpi")
            att_score   = c4.number_input("Attendance Score",  0, 100, 80, key="att_s")
            team_score  = c5.number_input("Teamwork Score",    0, 100, 78, key="team")
            prod_score  = c6.number_input("Productivity Score",0, 100, 82, key="prod")
            comments    = st.text_area("Manager Comments")

            if st.form_submit_button("💾 Save Appraisal"):
                overall = round((kpi_score + att_score + team_score + prod_score) / 4, 1)
                new_row = pd.DataFrame([{
                    "Name": name, "Department": dept,
                    "KPI Score": kpi_score, "Attendance Score": att_score,
                    "Teamwork Score": team_score, "Productivity Score": prod_score,
                    "Overall (%)": overall, "Grade": grade(overall), "Comments": comments
                }])
                if not perf_df.empty and name in perf_df["Name"].values:
                    perf_df.loc[perf_df["Name"] == name] = new_row.values
                else:
                    perf_df = pd.concat([perf_df, new_row], ignore_index=True)
                save_perf(perf_df, sel_month)
                st.success("Appraisal saved!")
                st.rerun()

        if not perf_df.empty:
            section(f"{sel_month} — Appraisal Records")
            st.dataframe(perf_df, use_container_width=True)

            avg_overall = perf_df["Overall (%)"].mean() if "Overall (%)" in perf_df else 0
            top_performer = perf_df.loc[perf_df["Overall (%)"].idxmax(), "Name"] if not perf_df.empty else "—"
            metric_row([
                ("Staff Appraised", len(perf_df)),
                ("Avg Overall Score", f"{avg_overall:.1f}%"),
                ("Top Performer", top_performer)
            ])

            csv_bytes = perf_df.to_csv(index=False).encode()
            st.download_button("⬇️ Download Report", csv_bytes,
                               f"Performance_{sel_month}.csv", "text/csv")
        else:
            st.info("No appraisal records for this month.")

    with tabs[1]:
        sel_month3 = st.selectbox("Select Month", months,
                                   index=date.today().month - 1, key="perf_month2")
        perf_df2 = load_perf(sel_month3)
        if not perf_df2.empty and "Overall (%)" in perf_df2.columns:
            try:
                import plotly.express as px
                fig = px.bar(perf_df2, x="Name", y="Overall (%)",
                             color="Grade", title=f"Staff Performance — {sel_month3}",
                             color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff")
                st.plotly_chart(fig, use_container_width=True)

                score_cols = ["KPI Score","Attendance Score","Teamwork Score","Productivity Score"]
                available  = [c for c in score_cols if c in perf_df2.columns]
                if available:
                    melt_df = perf_df2.melt(id_vars="Name", value_vars=available,
                                            var_name="Category", value_name="Score")
                    fig2 = px.bar(melt_df, x="Name", y="Score", color="Category",
                                  barmode="group", title="Score Breakdown by Employee",
                                  color_discrete_sequence=["#ff6b00","#1a1a1a","#666","#ccc"])
                    fig2.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff")
                    st.plotly_chart(fig2, use_container_width=True)
            except ImportError:
                st.dataframe(perf_df2, use_container_width=True)
        else:
            st.info("No data to visualise for this month.")

    with tabs[2]:
        section("All Performance Reports")
        all_perf = list(PERF_DIR.glob("*.csv")) if PERF_DIR.exists() else []
        if all_perf:
            combined = pd.concat([pd.read_csv(f).assign(Month=f.stem) for f in sorted(all_perf)], ignore_index=True)
            st.dataframe(combined, use_container_width=True)
            csv_bytes = combined.to_csv(index=False).encode()
            st.download_button("⬇️ Download All", csv_bytes, "Performance_All.csv", "text/csv")
        else:
            st.info("No reports found yet.")


# =========================================
# PAGE: ADMIN PANEL
# =========================================
def show_admin():
    page_header("🛠️ Admin Panel",
                "Administrative operations, consumables, meetings, stocks, and reports")
    ensure_admin()

    tabs = st.tabs(["🧴 Consumables", "📅 Meetings", "📦 Stock Records", "📄 Reports", "⚙️ Settings"])

    # ---- Consumables ----
    with tabs[0]:
        section("Consumables Records")
        CONS_FILE = ADMIN_DIR / "consumables.csv"
        if CONS_FILE.exists():
            cons_df = pd.read_csv(CONS_FILE)
        else:
            cons_df = pd.DataFrame({"Item": [], "Category": [], "Quantity": [],
                                    "Unit": [], "Date": [], "Requested By": [], "Status": []})

        with st.expander("➕ Add Consumable Record"):
            with st.form("cons_form"):
                c1, c2 = st.columns(2)
                item   = c1.text_input("Item Name")
                cat    = c2.selectbox("Category", ["Stationery","Cleaning","IT Supplies","Kitchen","Other"])
                c3, c4, c5 = st.columns(3)
                qty    = c3.number_input("Quantity", min_value=0)
                unit   = c4.text_input("Unit (e.g. pcs, packs)")
                req_by = c5.text_input("Requested By")
                status = st.selectbox("Status", ["Pending","Approved","Purchased","Delivered"])
                if st.form_submit_button("Add Record"):
                    new_row = pd.DataFrame([{
                        "Item": item, "Category": cat, "Quantity": qty,
                        "Unit": unit, "Date": str(date.today()),
                        "Requested By": req_by, "Status": status
                    }])
                    cons_df = pd.concat([cons_df, new_row], ignore_index=True)
                    cons_df.to_csv(CONS_FILE, index=False)
                    st.success("Record added!")
                    st.rerun()

        if not cons_df.empty:
            st.dataframe(cons_df, use_container_width=True)
            metric_row([("Total Items", len(cons_df)),
                        ("Pending", len(cons_df[cons_df["Status"]=="Pending"]) if "Status" in cons_df else 0)])
        else:
            st.info("No consumable records yet.")

    # ---- Meetings ----
    with tabs[1]:
        section("Meeting Records")
        MEET_FILE = MEETINGS_DIR / "meetings.csv"
        if MEET_FILE.exists():
            meet_df = pd.read_csv(MEET_FILE)
        else:
            meet_df = pd.DataFrame({"Title": [], "Date": [], "Time": [],
                                    "Venue": [], "Attendees": [], "Minutes": [], "Action Items": []})

        with st.expander("➕ Schedule / Record Meeting"):
            with st.form("meet_form"):
                c1, c2, c3 = st.columns(3)
                title   = c1.text_input("Meeting Title")
                meet_d  = c2.date_input("Date", key="meet_date")
                meet_t  = c3.time_input("Time", key="meet_time")
                c4, c5  = st.columns(2)
                venue   = c4.text_input("Venue")
                attend  = c5.text_input("Attendees (comma-separated)")
                minutes = st.text_area("Minutes / Notes")
                actions = st.text_area("Action Items")
                if st.form_submit_button("Save Meeting"):
                    new_row = pd.DataFrame([{
                        "Title": title, "Date": str(meet_d), "Time": str(meet_t),
                        "Venue": venue, "Attendees": attend, "Minutes": minutes, "Action Items": actions
                    }])
                    meet_df = pd.concat([meet_df, new_row], ignore_index=True)
                    meet_df.to_csv(MEET_FILE, index=False)
                    st.success("Meeting saved!")
                    st.rerun()

        # Upload meeting minutes docx
        st.markdown("**Upload Meeting Minutes (DOCX)**")
        uploaded_min = st.file_uploader("Upload .docx file", type=["docx"], key="meet_upload")
        if uploaded_min:
            save_path = MEETINGS_DIR / uploaded_min.name
            with open(save_path, "wb") as f:
                f.write(uploaded_min.read())
            st.success(f"'{uploaded_min.name}' uploaded to Meetings folder.")

        if not meet_df.empty:
            st.dataframe(meet_df, use_container_width=True)
        else:
            st.info("No meeting records yet.")

    # ---- Stock Records ----
    with tabs[2]:
        section("Stock Records")
        STOCK_FILE = STOCK_DIR / "stock.csv"
        if STOCK_FILE.exists():
            stock_df = pd.read_csv(STOCK_FILE)
        else:
            stock_df = pd.DataFrame({"Item": [], "Category": [], "Quantity In": [],
                                     "Quantity Out": [], "Balance": [], "Date": [], "Notes": []})

        with st.expander("➕ Add Stock Entry"):
            with st.form("stock_form"):
                c1, c2, c3 = st.columns(3)
                s_item = c1.text_input("Item Name")
                s_cat  = c2.text_input("Category")
                s_in   = c3.number_input("Quantity In", min_value=0)
                c4, c5, c6 = st.columns(3)
                s_out  = c4.number_input("Quantity Out", min_value=0)
                s_bal  = c5.number_input("Balance", min_value=0)
                s_note = c6.text_input("Notes")
                if st.form_submit_button("Add Stock"):
                    new_row = pd.DataFrame([{
                        "Item": s_item, "Category": s_cat, "Quantity In": s_in,
                        "Quantity Out": s_out, "Balance": s_bal,
                        "Date": str(date.today()), "Notes": s_note
                    }])
                    stock_df = pd.concat([stock_df, new_row], ignore_index=True)
                    stock_df.to_csv(STOCK_FILE, index=False)
                    st.success("Stock entry added!")
                    st.rerun()

        # Upload PDF report
        st.markdown("**Upload Stock PDF**")
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], key="stock_pdf")
        if uploaded_pdf:
            save_path = STOCK_DIR / uploaded_pdf.name
            with open(save_path, "wb") as f:
                f.write(uploaded_pdf.read())
            st.success(f"'{uploaded_pdf.name}' uploaded to Stock Records.")

        if not stock_df.empty:
            st.dataframe(stock_df, use_container_width=True)
            low_stock = stock_df[stock_df["Balance"] <= 5] if "Balance" in stock_df.columns else pd.DataFrame()
            if not low_stock.empty:
                st.warning(f"⚠️ {len(low_stock)} item(s) have low stock (balance ≤ 5).")
        else:
            st.info("No stock records yet.")

    # ---- Reports ----
    with tabs[3]:
        section("Reports")
        st.markdown("**Upload a Report**")
        report_type = st.selectbox("Report Type", ["General Report","HR Report","Finance Report","Operations Report"])
        uploaded_rep = st.file_uploader("Upload Report File (PDF/DOCX)", type=["pdf","docx"], key="rep_upload")
        if uploaded_rep:
            save_path = REPORTS_DIR / uploaded_rep.name
            with open(save_path, "wb") as f:
                f.write(uploaded_rep.read())
            st.success(f"'{uploaded_rep.name}' saved to Reports.")

        section("Existing Reports")
        rep_files = list(REPORTS_DIR.glob("*")) if REPORTS_DIR.exists() else []
        if rep_files:
            for rp in sorted(rep_files):
                col_a, col_b = st.columns([4, 1])
                col_a.markdown(f"📄 **{rp.name}**")
                with open(rp, "rb") as ff:
                    col_b.download_button("⬇️", ff.read(), file_name=rp.name, key=f"dl_{rp.name}")
        else:
            st.info("No reports uploaded yet.")

    # ---- Settings ----
    with tabs[4]:
        section("System Settings")
        st.markdown("""
        <div class="card">
            <h3>⚙️ Application Configuration</h3>
            <p>Manage system-wide settings, user access, and data backup options.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Company Information**")
        c1, c2 = st.columns(2)
        company  = c1.text_input("Company Name", value="Cardstel Solutions Limited")
        logo_up  = c2.file_uploader("Upload Logo", type=["png","jpg"], key="logo_upload")
        if logo_up:
            with open("logo.png", "wb") as f:
                f.write(logo_up.read())
            st.success("Logo updated! Refresh to see changes.")

        st.markdown("**Data Management**")
        if st.button("🗑️ Clear All Attendance Data (⚠️ Irreversible)"):
            import shutil
            if ATTENDANCE_DIR.exists():
                shutil.rmtree(ATTENDANCE_DIR)
                ATTENDANCE_DIR.mkdir()
            st.success("Attendance data cleared.")

        if st.button("📦 Backup All Data"):
            import zipfile, io
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as zf:
                for folder in [ATTENDANCE_DIR, LEAVE_DIR, BUSINESS_DIR, PERF_DIR, ADMIN_DIR, MEETINGS_DIR, REPORTS_DIR, STOCK_DIR]:
                    if folder.exists():
                        for ffile in folder.rglob("*"):
                            if ffile.is_file():
                                zf.write(ffile, ffile.relative_to(Path(".")))
                if EMPLOYEE_FILE.exists():
                    zf.write(EMPLOYEE_FILE)
            buf.seek(0)
            st.download_button("⬇️ Download Backup ZIP", buf.read(),
                               f"HR_Backup_{date.today()}.zip", "application/zip")

# =========================================
# MAIN ROUTER
# =========================================
# Handle home button navigation
if "_nav_target" in st.session_state:
    page = st.session_state.pop("_nav_target")

if page == "🏠 Home":
    show_home()
elif page == "📅 Attendance Management":
    show_attendance()
elif page == "💼 Business Department Appraisal":
    show_business()
elif page == "📝 Staff Performance Appraisal":
    show_performance()
elif page == "🛠️ Admin Panel":
    show_admin()
