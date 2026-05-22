import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import StringIO

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Daily Staff Report & Appraisal System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>
.main-title{
    font-size:36px;
    font-weight:bold;
    color:#1E3A8A;
}

.section-title{
    font-size:25px;
    font-weight:bold;
    color:#111827;
    margin-top:20px;
}

.metric-card{
    background-color:#F9FAFB;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# APP TITLE
# ==========================================================
st.markdown(
    '<div class="main-title">'
    'Daily Staff Report & Appraisal Dashboard'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================================
# FOLDER CONFIGURATION
# ==========================================================
REPORT_FOLDER = Path("daily_report")
REPORT_FOLDER.mkdir(exist_ok=True)

# ==========================================================
# GITHUB CONFIG
# ==========================================================
# REPLACE WITH YOUR DETAILS
GITHUB_USERNAME = "your_username"
GITHUB_REPO = "your_repo"
GITHUB_BRANCH = "main"

# Example:
# https://raw.githubusercontent.com/username/repo/main/daily_report/file.csv

BASE_GITHUB_URL = (
    f"https://raw.githubusercontent.com/"
    f"{GITHUB_USERNAME}/"
    f"{GITHUB_REPO}/"
    f"{GITHUB_BRANCH}/daily_report"
)

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================
REQUIRED_COLUMNS = [
    "Timestamp",
    "Name",
    "Employment Status",
    "Designation",
    "Department",
    "Reporting Line Manager/Supervisor",
    "Task 1 (Write out the task)",
    "Was Task 1 completed?",
    "Task 2 (Write out the task)",
    "Was task 2 completed?",
    "Challenges faced during the day"
]

# ==========================================================
# SCORE CALCULATOR
# ==========================================================
def calculate_score(response):

    if pd.isna(response):
        return 0

    response = str(response).strip().lower()

    if response == "yes":
        return 100

    elif response == "partially":
        return 50

    elif response == "no":
        return 0

    return 0


# ==========================================================
# PERFORMANCE CATEGORY
# ==========================================================
def classify_performance(score):

    if score >= 90:
        return "High Performer"

    elif score >= 60:
        return "Average Performer"

    return "Low Performer"


# ==========================================================
# LOAD CSV FILE
# ==========================================================
def load_csv(file_path):

    try:
        df = pd.read_csv(file_path)

        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = ""

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)


# ==========================================================
# SAVE CSV
# ==========================================================
def save_csv(df, filename):

    try:
        path = REPORT_FOLDER / filename
        df.to_csv(path, index=False)

    except Exception as e:
        st.error(f"Save Error: {e}")


# ==========================================================
# GET LOCAL REPORT FILES
# ==========================================================
def get_report_files():

    files = list(REPORT_FOLDER.glob("*.csv"))

    return sorted(
        [file.name for file in files],
        reverse=True
    )


# ==========================================================
# LOAD REPORT
# ==========================================================
def load_report(file_name):

    path = REPORT_FOLDER / file_name

    if path.exists():

        df = pd.read_csv(path)

        return df

    return pd.DataFrame()


# ==========================================================
# PREPROCESS DATA
# ==========================================================
def preprocess_dataframe(df):

    if df.empty:
        return df

    # Timestamp handling
    if "Timestamp" in df.columns:

        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

        df["Date"] = (
            df["Timestamp"]
            .dt.date
        )

        df["Month"] = (
            df["Timestamp"]
            .dt.strftime("%B")
        )

        df["Quarter"] = (
            df["Timestamp"]
            .dt.quarter
        )

    # Score calculation
    df["Task 1 Score"] = (
        df["Was Task 1 completed?"]
        .apply(calculate_score)
    )

    df["Task 2 Score"] = (
        df["Was task 2 completed?"]
        .apply(calculate_score)
    )

    df["Daily Score"] = (
        (
            df["Task 1 Score"]
            +
            df["Task 2 Score"]
        ) / 2
    )

    df["Performance"] = (
        df["Daily Score"]
        .apply(classify_performance)
    )

    return df


# ==========================================================
# GITHUB CSV DOWNLOAD
# ==========================================================
def download_csv_from_github(filename):

    url = f"{BASE_GITHUB_URL}/{filename}"

    try:
        response = requests.get(url)

        if response.status_code == 200:

            df = pd.read_csv(
                StringIO(response.text)
            )

            save_csv(df, filename)

            return True

        return False

    except:
        return False


# ==========================================================
# SYNC DAILY REPORTS
# ==========================================================
def sync_github_reports():

    st.info(
        "Upload daily CSV reports to GitHub "
        "daily_report folder."
    )

    # Expected naming:
    # 2026-05-01.csv
    # 2026-05-02.csv

    today = datetime.today()

    current_month = today.month
    current_year = today.year

    for day in range(1, 32):

        try:

            filename = (
                f"{current_year}-"
                f"{current_month:02d}-"
                f"{day:02d}.csv"
            )

            local_file = (
                REPORT_FOLDER / filename
            )

            if not local_file.exists():

                download_csv_from_github(
                    filename
                )

        except:
            pass


# ==========================================================
# INITIAL DATA SYNC
# ==========================================================
sync_github_reports()

# ==========================================================
# SIDEBAR MENU
# ==========================================================
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Menu",
    [
        "Dashboard",
        "Daily Report",
        "Appraisal"
    ]
)

# ==========================================================
# DASHBOARD
# ==========================================================
if menu == "Dashboard":

    st.markdown(
        '<div class="section-title">'
        'Dashboard Overview'
        '</div>',
        unsafe_allow_html=True
    )

    report_files = get_report_files()

    total_reports = len(report_files)

    all_data = []

    for file in report_files:

        try:
            df = load_report(file)

            if not df.empty:
                all_data.append(df)

        except:
            pass

    if all_data:

        master_df = pd.concat(
            all_data,
            ignore_index=True
        )

        master_df = preprocess_dataframe(
            master_df
        )

        total_staff = (
            master_df["Name"]
            .nunique()
        )

        avg_score = round(
            master_df["Daily Score"]
            .mean(),
            2
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Reports",
                total_reports
            )

        with col2:
            st.metric(
                "Total Staff",
                total_staff
            )

        with col3:
            st.metric(
                "Average Score",
                avg_score
            )

    else:
        st.warning(
            "No reports found."
        )

# ==========================================================
# DAILY REPORT SECTION
# ==========================================================
elif menu == "Daily Report":

    st.markdown(
        '<div class="section-title">'
        'Daily Report Viewer'
        '</div>',
        unsafe_allow_html=True
    )

    report_files = get_report_files()

    if len(report_files) == 0:

        st.warning(
            "No daily reports found."
        )

    else:

        selected_report = st.selectbox(
            "Select Daily Report",
            report_files
        )

        df = load_report(
            selected_report
        )

        if not df.empty:

            df = preprocess_dataframe(df)

            st.success(
                f"Viewing "
                f"{selected_report}"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader(
                "Quick Summary"
            )

            col1, col2, col3 = (
                st.columns(3)
            )

            with col1:
                st.metric(
                    "Staff Count",
                    df["Name"]
                    .nunique()
                )

            with col2:
                st.metric(
                    "Avg Score",
                    round(
                        df[
                            "Daily Score"
                        ].mean(),
                        2
                    )
                )

            with col3:
                st.metric(
                    "High Performers",
                    len(
                        df[
                            df[
                                "Performance"
                            ]
                            ==
                            "High Performer"
                        ]
                    )
                )

        else:
            st.error(
                "Unable to load report."
            )

# ==========================================================
# APPRAISAL PLACEHOLDER
# ==========================================================
elif menu == "Appraisal":

    st.markdown(
        '<div class="section-title">'
        'Monthly & Quarterly Appraisal'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Appraisal analytics "
        "coming in PART 2"
    )
    # ==========================================================
# PART 2
# STAFF RATING + ANALYTICS + CHARTS
# ==========================================================

# ==========================================================
# LOAD MASTER DATA
# ==========================================================
def load_master_data():

    report_files = get_report_files()

    all_data = []

    for file in report_files:

        try:
            df = load_report(file)

            if not df.empty:
                all_data.append(df)

        except:
            pass

    if len(all_data) == 0:
        return pd.DataFrame()

    master_df = pd.concat(
        all_data,
        ignore_index=True
    )

    master_df = preprocess_dataframe(
        master_df
    )

    return master_df


# ==========================================================
# EMPLOYEE PERFORMANCE SUMMARY
# ==========================================================
def employee_summary(df):

    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("Name")
        .agg({
            "Department": "first",
            "Designation": "first",
            "Daily Score": "mean",
            "Performance": lambda x:
                x.value_counts().index[0]
        })
        .reset_index()
    )

    summary["Daily Score"] = (
        summary["Daily Score"]
        .round(2)
    )

    summary["Rank"] = (
        summary["Daily Score"]
        .rank(
            ascending=False,
            method="dense"
        )
    )

    summary = summary.sort_values(
        "Daily Score",
        ascending=False
    )

    return summary


# ==========================================================
# DEPARTMENT PERFORMANCE
# ==========================================================
def department_summary(df):

    if df.empty:
        return pd.DataFrame()

    dept_df = (
        df.groupby("Department")
        .agg({
            "Daily Score": "mean"
        })
        .reset_index()
    )

    dept_df["Daily Score"] = (
        dept_df["Daily Score"]
        .round(2)
    )

    return dept_df


# ==========================================================
# MONTHLY PERFORMANCE
# ==========================================================
def monthly_summary(df):

    if df.empty:
        return pd.DataFrame()

    monthly = (
        df.groupby(["Month", "Name"])
        .agg({
            "Daily Score": "mean"
        })
        .reset_index()
    )

    monthly["Daily Score"] = (
        monthly["Daily Score"]
        .round(2)
    )

    return monthly


# ==========================================================
# QUARTERLY PERFORMANCE
# ==========================================================
def quarterly_summary(df):

    if df.empty:
        return pd.DataFrame()

    quarterly = (
        df.groupby(
            ["Quarter", "Name"]
        )
        .agg({
            "Daily Score": "mean"
        })
        .reset_index()
    )

    quarterly["Daily Score"] = (
        quarterly["Daily Score"]
        .round(2)
    )

    return quarterly


# ==========================================================
# DASHBOARD CHARTS
# ==========================================================
if menu == "Dashboard":

    master_df = load_master_data()

    if not master_df.empty:

        st.markdown("---")
        st.subheader(
            "Performance Analytics"
        )

        # ====================================
        # PIE CHART
        # ====================================
        performance_counts = (
            master_df["Performance"]
            .value_counts()
            .reset_index()
        )

        performance_counts.columns = [
            "Performance",
            "Count"
        ]

        pie_fig = px.pie(
            performance_counts,
            names="Performance",
            values="Count",
            title="Staff Performance"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

        # ====================================
        # DEPARTMENT BAR CHART
        # ====================================
        dept_df = department_summary(
            master_df
        )

        dept_fig = px.bar(
            dept_df,
            x="Department",
            y="Daily Score",
            title="Department Performance"
        )

        st.plotly_chart(
            dept_fig,
            use_container_width=True
        )

        # ====================================
        # MONTHLY TREND
        # ====================================
        month_trend = (
            master_df.groupby("Month")
            ["Daily Score"]
            .mean()
            .reset_index()
        )

        line_fig = px.line(
            month_trend,
            x="Month",
            y="Daily Score",
            markers=True,
            title="Monthly Performance Trend"
        )

        st.plotly_chart(
            line_fig,
            use_container_width=True
        )

        # ====================================
        # TOP STAFF
        # ====================================
        st.subheader(
            "Top Performers"
        )

        summary = employee_summary(
            master_df
        )

        top_staff = summary.head(10)

        st.dataframe(
            top_staff,
            use_container_width=True
        )

        top_fig = px.bar(
            top_staff,
            x="Name",
            y="Daily Score",
            title="Top 10 Performers"
        )

        st.plotly_chart(
            top_fig,
            use_container_width=True
        )

        # ====================================
        # LOW PERFORMERS
        # ====================================
        st.subheader(
            "Low Performers"
        )

        low_staff = summary[
            summary["Daily Score"] < 60
        ]

        st.dataframe(
            low_staff,
            use_container_width=True
        )

        if not low_staff.empty:

            low_fig = px.bar(
                low_staff,
                x="Name",
                y="Daily Score",
                title="Low Performers"
            )

            st.plotly_chart(
                low_fig,
                use_container_width=True
            )

# ==========================================================
# DAILY REPORT ANALYTICS
# ==========================================================
elif menu == "Daily Report":

    report_files = get_report_files()

    if len(report_files) > 0:

        selected_report = st.selectbox(
            "Select Daily Report",
            report_files,
            key="report_select_2"
        )

        df = load_report(
            selected_report
        )

        if not df.empty:

            df = preprocess_dataframe(
                df
            )

            st.markdown("---")
            st.subheader(
                "Daily Analytics"
            )

            # ====================================
            # PERFORMANCE CHART
            # ====================================
            performance_fig = px.bar(
                df,
                x="Name",
                y="Daily Score",
                color="Performance",
                title="Staff Daily Rating"
            )

            st.plotly_chart(
                performance_fig,
                use_container_width=True
            )

            # ====================================
            # TASK COMPLETION PIE
            # ====================================
            completed = len(
                df[
                    df[
                        "Performance"
                    ]
                    ==
                    "High Performer"
                ]
            )

            partial = len(
                df[
                    df[
                        "Performance"
                    ]
                    ==
                    "Average Performer"
                ]
            )

            low = len(
                df[
                    df[
                        "Performance"
                    ]
                    ==
                    "Low Performer"
                ]
            )

            pie_df = pd.DataFrame({
                "Status": [
                    "High",
                    "Average",
                    "Low"
                ],
                "Count": [
                    completed,
                    partial,
                    low
                ]
            })

            pie_chart = px.pie(
                pie_df,
                names="Status",
                values="Count",
                title="Daily Performance"
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

            # ====================================
            # DEPARTMENT PERFORMANCE
            # ====================================
            dept_day = (
                df.groupby("Department")
                ["Daily Score"]
                .mean()
                .reset_index()
            )

            dept_chart = px.bar(
                dept_day,
                x="Department",
                y="Daily Score",
                title="Department Daily Score"
            )

            st.plotly_chart(
                dept_chart,
                use_container_width=True
            )

            # ====================================
            # STAFF RANKING
            # ====================================
            st.subheader(
                "Daily Staff Ranking"
            )

            rank_df = (
                df[
                    [
                        "Name",
                        "Department",
                        "Daily Score",
                        "Performance"
                    ]
                ]
                .sort_values(
                    "Daily Score",
                    ascending=False
                )
            )

            st.dataframe(
                rank_df,
                use_container_width=True
            )
            # ==========================================================
# PART 3
# APPRAISAL SYSTEM (MONTHLY + QUARTERLY)
# ==========================================================

elif menu == "Appraisal":

    st.markdown(
        '<div class="section-title">Appraisal Dashboard</div>',
        unsafe_allow_html=True
    )

    master_df = load_master_data()

    if master_df.empty:
        st.warning("No data available for appraisal analysis.")
        st.stop()

    # ======================================================
    # MONTHLY APPRAISAL
    # ======================================================
    st.subheader("Monthly Appraisal")

    monthly_df = (
        master_df.groupby(["Month", "Name"])
        .agg({
            "Daily Score": "mean",
            "Department": "first",
            "Designation": "first"
        })
        .reset_index()
    )

    monthly_df["Daily Score"] = monthly_df["Daily Score"].round(2)

    # Rank staff monthly
    monthly_df["Rank"] = (
        monthly_df.groupby("Month")["Daily Score"]
        .rank(ascending=False, method="dense")
    )

    # Performance category
    monthly_df["Performance"] = monthly_df["Daily Score"].apply(classify_performance)

    selected_month = st.selectbox(
        "Select Month",
        sorted(monthly_df["Month"].dropna().unique())
    )

    month_data = monthly_df[monthly_df["Month"] == selected_month]

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Monthly Score", round(month_data["Daily Score"].mean(), 2))
    col2.metric("High Performers", len(month_data[month_data["Performance"] == "High Performer"]))
    col3.metric("Low Performers", len(month_data[month_data["Performance"] == "Low Performer"]))

    st.dataframe(month_data.sort_values("Daily Score", ascending=False), use_container_width=True)

    # Monthly chart
    monthly_fig = px.bar(
        month_data,
        x="Name",
        y="Daily Score",
        color="Performance",
        title=f"Monthly Performance - {selected_month}"
    )
    st.plotly_chart(monthly_fig, use_container_width=True)

    # Pie chart
    monthly_pie = px.pie(
        month_data,
        names="Performance",
        title="Monthly Performance Distribution"
    )
    st.plotly_chart(monthly_pie, use_container_width=True)

    # Department performance monthly
    dept_month = (
        month_data.groupby("Department")["Daily Score"]
        .mean()
        .reset_index()
    )

    dept_month_fig = px.bar(
        dept_month,
        x="Department",
        y="Daily Score",
        title="Monthly Department Performance"
    )
    st.plotly_chart(dept_month_fig, use_container_width=True)

    # ======================================================
    # QUARTERLY APPRAISAL
    # ======================================================
    st.subheader("Quarterly Appraisal")

    quarterly_df = (
        master_df.groupby(["Quarter", "Name"])
        .agg({
            "Daily Score": "mean",
            "Department": "first",
            "Designation": "first"
        })
        .reset_index()
    )

    quarterly_df["Daily Score"] = quarterly_df["Daily Score"].round(2)

    quarterly_df["Rank"] = (
        quarterly_df.groupby("Quarter")["Daily Score"]
        .rank(ascending=False, method="dense")
    )

    quarterly_df["Performance"] = quarterly_df["Daily Score"].apply(classify_performance)

    selected_quarter = st.selectbox(
        "Select Quarter",
        sorted(quarterly_df["Quarter"].dropna().unique())
    )

    quarter_data = quarterly_df[quarterly_df["Quarter"] == selected_quarter]

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Quarterly Score", round(quarter_data["Daily Score"].mean(), 2))
    col2.metric("High Performers", len(quarter_data[quarter_data["Performance"] == "High Performer"]))
    col3.metric("Low Performers", len(quarter_data[quarter_data["Performance"] == "Low Performer"]))

    st.dataframe(quarter_data.sort_values("Daily Score", ascending=False), use_container_width=True)

    # Quarterly bar chart
    quarterly_fig = px.bar(
        quarter_data,
        x="Name",
        y="Daily Score",
        color="Performance",
        title=f"Quarterly Performance - Q{selected_quarter}"
    )
    st.plotly_chart(quarterly_fig, use_container_width=True)

    # Quarterly pie chart
    quarterly_pie = px.pie(
        quarter_data,
        names="Performance",
        title="Quarterly Performance Distribution"
    )
    st.plotly_chart(quarterly_pie, use_container_width=True)

    # Department quarterly
    dept_quarter = (
        quarter_data.groupby("Department")["Daily Score"]
        .mean()
        .reset_index()
    )

    dept_quarter_fig = px.bar(
        dept_quarter,
        x="Department",
        y="Daily Score",
        title="Quarterly Department Performance"
    )
    st.plotly_chart(dept_quarter_fig, use_container_width=True)

    # ======================================================
    # OVERALL APPRAISAL SUMMARY
    # ======================================================
    st.subheader("Overall Staff Appraisal Summary")

    appraisal_summary = (
        master_df.groupby("Name")
        .agg({
            "Daily Score": "mean",
            "Department": "first",
            "Designation": "first"
        })
        .reset_index()
    )

    appraisal_summary["Daily Score"] = appraisal_summary["Daily Score"].round(2)

    appraisal_summary["Performance"] = appraisal_summary["Daily Score"].apply(classify_performance)

    appraisal_summary = appraisal_summary.sort_values("Daily Score", ascending=False)

    st.dataframe(appraisal_summary, use_container_width=True)

    # Top vs Low performers pie
    perf_summary = appraisal_summary["Performance"].value_counts().reset_index()
    perf_summary.columns = ["Performance", "Count"]

    perf_fig = px.pie(
        perf_summary,
        names="Performance",
        values="Count",
        title="Overall Performance Distribution"
    )
    st.plotly_chart(perf_fig, use_container_width=True)

    # ======================================================
    # FINAL LEADERBOARD
    # ======================================================
    st.subheader("Final Leaderboard")

    leaderboard = appraisal_summary.head(10)

    leaderboard_fig = px.bar(
        leaderboard,
        x="Name",
        y="Daily Score",
        color="Performance",
        title="Top 10 Staff Overall"
    )

    st.plotly_chart(leaderboard_fig, use_container_width=True)
