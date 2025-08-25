import streamlit as st
import json
from pathlib import Path
from datetime import datetime


# --- Page Config ---
st.set_page_config(
    page_title="Competitor Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }

    .competitor-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }

    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.25rem;
    }

    .status-updated {
        background: #d4edda;
        color: #155724;
    }

    .status-no-change {
        background: #fff3cd;
        color: #856404;
    }

    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Project root ---
project_root = Path(__file__).parent.parent.resolve()
report_dir = project_root / "data" / "reports"


# Utility functions
def get_latest_report():
    files = list(report_dir.glob("*.json"))
    if not files:
        return None
    latest_file = max(files, key=lambda f: f.stat().st_ctime)
    return latest_file


def get_status_badge(update_text):
    if "updated" in update_text.lower() or "new" in update_text.lower():
        return "status-updated"
    return "status-no-change"


def parse_date(date_str):
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return None


# --- Main App ---
st.markdown('<h1 class="main-header">📊 Competitor Intelligence Dashboard</h1>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("🔍 Filters & Controls")

    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

    st.markdown(
        '<div class="sidebar-info"><strong>ℹ️ Info:</strong><br>This dashboard shows the latest competitor intelligence data. Use filters below to focus on specific competitors or dates.</div>',
        unsafe_allow_html=True)

# Load data
latest_report = get_latest_report()

if latest_report:
    with open(latest_report, "r", encoding="utf-8") as report_file:
        data = json.load(report_file)

    competitors = data.get("competitors", [])

    if competitors:
        # --- Sidebar Filters ---
        with st.sidebar:
            competitor_names = [c["name"] for c in competitors]
            selected_name = st.selectbox("🏢 Filter by Competitor:", ["All"] + competitor_names)

            dates = [c.get("last_updated", "")[:10] for c in competitors if c.get("last_updated")]
            unique_dates = sorted(list(set(dates)), reverse=True)
            selected_date = st.selectbox("📅 Filter by Date:", ["All"] + unique_dates)

            st.markdown("---")
            st.subheader("📈 Quick Stats")
            total_competitors = len(competitors)
            updated_today = len(
                [c for c in competitors if c.get("last_updated", "")[:10] == datetime.now().strftime("%Y-%m-%d")])

            st.metric("Total Competitors", total_competitors)
            st.metric("Updated Today", updated_today)

        # --- Main Content ---
        st.info(
            f"📁 **Data Source:** {latest_report.name} | **Last Modified:** {datetime.fromtimestamp(latest_report.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")

        # Filter competitors
        filtered_competitors = []
        for competitor in competitors:
            name_match = (selected_name == "All") or (competitor["name"] == selected_name)
            date_match = (selected_date == "All") or (competitor.get("last_updated", "")[:10] == selected_date)
            if name_match and date_match:
                filtered_competitors.append(competitor)

        if not filtered_competitors:
            st.warning("🔍 No competitors match your current filters.")
        else:
            # --- Summary Cards ---
            st.subheader("📊 Overview")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h3>{len(filtered_competitors)}</h3>
                    <p>Competitors Showing</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                recent_updates = len(
                    [c for c in filtered_competitors if "updated" in str(c.get("website_update", "")).lower()])
                st.markdown(f"""
                <div class="metric-container">
                    <h3>{recent_updates}</h3>
                    <p>Recent Website Updates</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                app_updates = len(
                    [c for c in filtered_competitors if "updated" in str(c.get("app_update", "")).lower()])
                st.markdown(f"""
                <div class="metric-container">
                    <h3>{app_updates}</h3>
                    <p>Recent App Updates</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # --- Competitor Cards ---
            st.subheader("🏢 Competitor Details")

            for i, competitor in enumerate(filtered_competitors):
                with st.expander(f"🏢 {competitor['name']}", expanded=i < 3):  # Auto-expand first 3
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"""
                        <div class="competitor-card">
                            <h4>{competitor['name']}</h4>
                            <p><strong>🌐 Website:</strong> {competitor.get('website_update', 'N/A')}</p>
                            <p><strong>📱 App:</strong> {competitor.get('app_update', 'N/A')}</p>
                            <p><strong>💬 Social:</strong> {competitor.get('social_update', 'N/A')}</p>
                            <p><strong>🕒 Last Updated:</strong> {competitor.get('last_updated', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        # Status badges
                        st.markdown("**Status:**")
                        website_status = get_status_badge(competitor.get('website_update', ''))
                        app_status = get_status_badge(competitor.get('app_update', ''))
                        social_status = get_status_badge(competitor.get('social_update', ''))

                        st.markdown(f"""
                        <span class="status-badge {website_status}">Website</span><br>
                        <span class="status-badge {app_status}">App</span><br>
                        <span class="status-badge {social_status}">Social</span>
                        """, unsafe_allow_html=True)

                        # Quick actions
                        st.markdown("**Quick Actions:**")
                        if st.button(f"📋 Export {competitor['name']}", key=f"export_{i}"):
                            st.download_button(
                                "Download JSON",
                                json.dumps(competitor, indent=2),
                                f"{competitor['name'].replace(' ', '_')}_data.json",
                                "application/json"
                            )

    else:
        st.error("❌ No competitor data found in the report file.")

else:
    st.error("❌ No reports found in data/reports. Please run the collector first.")
    st.markdown("""
    ### 🚀 Getting Started
    1. Run your data collector to generate report files
    2. Ensure reports are saved in `data/reports/` directory
    3. Refresh this dashboard to see the latest data
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>Competitor Intelligence Dashboard | Built with Streamlit | 📊 Data-driven insights</small>
</div>
""", unsafe_allow_html=True)