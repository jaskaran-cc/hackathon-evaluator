import streamlit as st
import os

# --- Page Config ---
st.set_page_config(page_title="Hackathon Evaluator", layout="wide")

# --- Sidebar for navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Evaluation", "Leaderboard"])

CSV_FILE = "evaluation_results.csv"

# --- Evaluation Page ---
if page == "Evaluation":
    import requests
    import pandas as pd
    import plotly.graph_objects as go
    from datetime import datetime

    # Header with logo
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("images/cc_logo.jpg", width=200)
    with col2:
        st.title("Hackathon Evaluation Dashboard")

    # Max points per category
    category_max = {
        "Innovation": 25,
        "Technical": 25,
        "Feasibility": 20,
        "Impact": 15,
        "Presentation": 15
    }

    # Input
    repo_url = st.text_input("Enter GitHub repository URL:")
    team_name = st.text_input("Enter Team Name (optional)")

    if st.button("Evaluate"):
        if not repo_url.strip():
            st.warning("⚠️ Please enter a valid GitHub repository URL.")
            st.stop()

        with st.spinner("Running evaluation..."):
            try:
                response = requests.post(
                    "http://localhost:8000/evaluate",
                    json={"repo_url": repo_url},
                    timeout=300
                )
                report = response.json()
            except Exception as e:
                st.error(f"❌ Error calling evaluation API: {e}")
                st.stop()

        total_score = report.get("total_score", 0)
        st.success(f"✅ Total Score: {total_score}/100")

        # Show gauges and feedback
        st.markdown("---")
        for cat, val in report["details"].items():
            st.subheader(f"{cat} (Score: {val['score']}/{category_max[cat]})")
            st.write(val["feedback"])

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val["score"],
                number={'suffix': f"/{category_max[cat]}"},
                title={'text': cat, 'font': {'size': 18}},
                gauge={
                    'axis': {'range': [0, category_max[cat]]},
                    'bar': {'color': "#003366"},
                    'steps': [
                        {'range': [0, category_max[cat]*0.5], 'color': "#f4cccc"},
                        {'range': [category_max[cat]*0.5, category_max[cat]*0.8], 'color': "#ffe599"},
                        {'range': [category_max[cat]*0.8, category_max[cat]], 'color': "#d9ead3"}
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

        # Save results to CSV
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "github_url": repo_url,
            "team_name": team_name if team_name.strip() else "",
            "total_score": total_score,
        }
        for cat, val in report["details"].items():
            data[cat] = val["score"]

        df_new = pd.DataFrame([data])
        if os.path.exists(CSV_FILE):
            df_existing = pd.read_csv(CSV_FILE)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(CSV_FILE, index=False)
        else:
            df_new.to_csv(CSV_FILE, index=False)

        st.success("📊 Results saved to leaderboard data!")

# --- Leaderboard Page ---
elif page == "Leaderboard":
    import pandas as pd

    st.title("🏆 Hackathon Leaderboard")

    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            st.info("No evaluation data yet. Please evaluate some repositories first.")
        else:
            # Sort by total score
            df = df.sort_values(by="total_score", ascending=False).reset_index(drop=True)

            st.subheader("📋 Evaluation Results")
            st.dataframe(
                df.style.background_gradient(cmap="Blues").format(precision=1),
                use_container_width=True
            )

            # Bar chart of total scores
            st.subheader("📊 Total Scores Comparison")
            st.bar_chart(df.set_index("team_name")["total_score"])

            # Highlight top project
            top_repo = df.iloc[0]
            st.markdown(
                f"### 🥇 Top Project: **{top_repo['team_name']}** — {top_repo['total_score']}/100"
            )

            # Download CSV button
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Leaderboard CSV", csv, "evaluation_results.csv", "text/csv")

    except FileNotFoundError:
        st.warning("⚠️ No leaderboard data file found. Please run evaluations first.")
