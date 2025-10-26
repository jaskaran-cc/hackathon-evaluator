import streamlit as st
import requests
import plotly.graph_objects as go
import streamlit as st

# Create two columns: logo on left, title on right
col1, col2 = st.columns([1, 5])  # Adjust ratio for size

with col1:
    st.image("images/cc_logo.jpg", width=500)  # Replace with your logo path

with col2:
    st.title("Hackathon Evaluation")

# st.title("Hackathon Evaluation Dashboard")

# Maximum points for each category
category_max = {
    "Innovation": 25,
    "Technical": 25,
    "Feasibility": 20,
    "Impact": 15,
    "Presentation": 15
}

repo_url = st.text_input("Enter GitHub repository URL:")

if st.button("Evaluate"):
    with st.spinner("Running multi-agent evaluation..."):
        response = requests.post(
            "http://localhost:8000/evaluate",
            json={"repo_url": repo_url}
        )
        report = response.json()

    st.success(f"Total Score: {report['total_score']}/100")

    # Display gauges for each category
    for cat, val in report["details"].items():
        print("category:",cat)
        st.subheader(f"{cat} (Score: {val['score']}/{category_max[cat]})")
        st.write(val["feedback"])

        # Create a speedometer/gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val["score"],
            number={'suffix': f"/{category_max[cat]}"},
            title={'text': cat},
            gauge={
                'axis': {'range': [0, category_max[cat]]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, category_max[cat]*0.5], 'color': "red"},
                    {'range': [category_max[cat]*0.5, category_max[cat]*0.8], 'color': "yellow"},
                    {'range': [category_max[cat]*0.8, category_max[cat]], 'color': "green"}
                ],
            }
        ))

        st.plotly_chart(fig)
