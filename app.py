import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Monthly Appraisal Dashboard",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
<style>

.stApp{
    background-color:white;
}

.main-title{
    font-size:38px;
    font-weight:bold;
    color:#ff7a00;
}

.metric-card{
    background: linear-gradient(
    135deg,
    #ff9a3c,
    #ff6b00
    );
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.15);
}

.chart-box{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.10);
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================
st.markdown(
    '<p class="main-title">📊 Monthly Appraisal Dashboard</p>',
    unsafe_allow_html=True
)

st.write(
    "Upload employee KPI CSV file for automatic appraisal scoring."
)

# ======================================================
# KPI TARGETS & WEIGHTS
# ======================================================
kpi_targets = {
    "Lead Generation": 100,
    "Client Acquisition": 10,
    "Revenue Growth": 5000000,
    "Client Conversion": 30,
    "Pipeline Management": 10000000,
    "Proposal Success": 40,
    "Client Retention": 90,
    "Customer Relationship": 5,
    "Business Expansion": 2,
    "Reporting & Compliance": 100,
    "Team Collaboration": 100,
    "Professional Conduct": 100
}

kpi_weights = {
    "Lead Generation": 10,
    "Client Acquisition": 10,
    "Revenue Growth": 15,
    "Client Conversion": 10,
    "Pipeline Management": 10,
    "Proposal Success": 10,
    "Client Retention": 10,
    "Customer Relationship": 5,
    "Business Expansion": 5,
    "Reporting & Compliance": 5,
    "Team Collaboration": 5,
    "Professional Conduct": 5
}

# ======================================================
# FILE UPLOAD
# ======================================================
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ==================================================
    # CALCULATE SCORES
    # ==================================================
    total_scores = []

    for _, row in df.iterrows():

        total_score = 0

        for kpi in kpi_targets.keys():

            actual = row[kpi]
            target = kpi_targets[kpi]
            weight = kpi_weights[kpi]

            achievement = (
                actual / target
            ) * 100

            achievement = min(
                achievement,
                100
            )

            weighted_score = (
                achievement * weight
            ) / 100

            total_score += weighted_score

        total_scores.append(
            round(total_score, 2)
        )

    df["Final Score (%)"] = total_scores

    # ==================================================
    # PERFORMANCE RATING
    # ==================================================
    def performance_rating(score):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Very Good"

        elif score >= 60:
            return "Good"

        elif score >= 50:
            return "Average"

        else:
            return "Poor"

    df["Performance Rating"] = df[
        "Final Score (%)"
    ].apply(performance_rating)

    # ==================================================
    # KPI CARDS
    # ======================================================
    total_staff = len(df)
    avg_score = round(
        df["Final Score (%)"].mean(),
        2
    )
    top_score = round(
        df["Final Score (%)"].max(),
        2
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{total_staff}</h2>
            <p>Total Employees</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{avg_score}%</h2>
            <p>Average Score</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{top_score}%</h2>
            <p>Top Score</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # CHARTS
    # ======================================================
    col1, col2 = st.columns(2)

    # PIE CHART
    with col1:

        rating_counts = df[
            "Performance Rating"
        ].value_counts().reset_index()

        rating_counts.columns = [
            "Rating",
            "Count"
        ]

        fig_pie = px.pie(
            rating_counts,
            names="Rating",
            values="Count",
            title="Performance Rating Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    # HISTOGRAM
    with col2:

        fig_hist = px.histogram(
            df,
            x="Final Score (%)",
            nbins=10,
            title="Employee Score Distribution",
            color_discrete_sequence=["#ff7a00"]
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    # ==================================================
    # TOP PERFORMERS
    # ======================================================
    st.subheader("🏆 Top Employees")

    top_10 = df.sort_values(
        "Final Score (%)",
        ascending=False
    ).head(10)

    fig_bar = px.bar(
        top_10,
        x="Employee Name",
        y="Final Score (%)",
        color="Final Score (%)",
        text="Final Score (%)",
        title="Top 10 Employee Performance",
        color_continuous_scale="Sunset"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # ==================================================
    # KPI AVERAGE PERFORMANCE
    # ======================================================
    st.subheader(
        "📈 KPI Average Performance"
    )

    kpi_avg = {}

    for kpi in kpi_targets.keys():
        kpi_avg[kpi] = df[kpi].mean()

    avg_df = pd.DataFrame({
        "KPI": kpi_avg.keys(),
        "Average": kpi_avg.values()
    })

    fig_kpi = px.bar(
        avg_df,
        x="KPI",
        y="Average",
        color="Average",
        title="Average KPI Performance",
        color_continuous_scale="Oranges"
    )

    st.plotly_chart(
        fig_kpi,
        use_container_width=True
    )

    # ==================================================
    # DATA TABLE
    # ======================================================
    st.subheader(
        "📋 Monthly Appraisal Results"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # ==================================================
    # DOWNLOAD
    # ======================================================
    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Appraisal Report",
        data=csv,
        file_name="monthly_appraisal_results.csv",
        mime="text/csv"
    )
