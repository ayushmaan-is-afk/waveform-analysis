import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page config
st.set_page_config(
    page_title="DCRM Anomaly Detection",
    page_icon="⚡",
    layout="wide"
)

# Title
st.title("⚡ DCRM Anomaly Detection System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", [
        "Predict",
        "History",
        "About"
    ])
    
    st.markdown("---")
    st.caption("DCRM Anomaly Detection v1.0")

# ─────────────────────────────────────
# PAGE 1 - PREDICT
# ─────────────────────────────────────
if page == "Predict":
    st.header("Upload DCRM File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your DCRM CSV file",
        type=['csv'],
        help="Upload a DCRM test file to analyze"
    )
    
    if uploaded_file:
        st.info(f"📁 File uploaded: {uploaded_file.name}")
        
        if st.button("🔬 Analyze", use_container_width=True):
            with st.spinner("Analyzing..."):
                try:
                    # Call FastAPI
                    response = requests.post(
                        'http://localhost:8000/dcrm/predict',
                        files={'file': uploaded_file}
                    )
                    result = response.json()
                    
                    st.markdown("---")
                    st.subheader("Results")
                    
                    # Status
                    col1, col2, col3 = st.columns(3)
                    🔍 
                    with col1:
                        if result['status'] == 'FAULTY':
                            st.error(f"❌ {result['status']}")
                        elif result['status'] == 'DEGRADING':
                            st.warning(f"⚠️ {result['status']}")
                        else:
                            st.success(f"✅ {result['status']}")
                    
                    with col2:
                        st.metric(
                            "Anomaly %",
                            f"{result['anomaly_percent']:.1f}%"
                        )
                    
                    with col3:
                        st.metric(
                            "Anomaly Score",
                            f"{result['anomaly_score']:.4f}"
                        )
                    
                    st.markdown("---")
                    
                    # Faulty components
                    if result.get('faulty_components'):
                        st.subheader("⚠️ Faulty Components")
                        
                        components = result['faulty_components']
                        comp_df = pd.DataFrame({
                            'Component' : list(components.keys()),
                            'Severity'  : list(components.values())
                        }).sort_values('Severity')
                        
                        st.dataframe(comp_df, use_container_width=True)
                        
                        # Bar chart
                        fig, ax = plt.subplots(figsize=(8, 4))
                        ax.barh(
                            comp_df['Component'],
                            comp_df['Severity'],
                            color='red',
                            alpha=0.7
                        )
                        ax.set_xlabel('Severity Score')
                        ax.set_title('Faulty Components')
                        st.pyplot(fig)
                    
                    # Maintenance recommendations
                    if result.get('maintenance_recs'):
                        st.subheader("🔧 Maintenance Recommendations")
                        for component, rec in result['maintenance_recs'].items():
                            st.write(f"**{component}:** {rec}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.warning("Make sure FastAPI server is running on port 8000")


# ─────────────────────────────────────
# PAGE 2 - HISTORY
# ─────────────────────────────────────
elif page == "History":
    st.header("Breaker History")
    
    breaker_id = st.text_input(
        "Enter Breaker ID",
        placeholder="e.g. 402"
    )
    
    if st.button("Search", use_container_width=True):
        if breaker_id:
            with st.spinner("Searching..."):
                try:
                    response = requests.get(
                        f'http://localhost:8000/dcrm/history/{breaker_id}'
                    )
                    result = response.json()
                    
                    if result['history']:
                        st.success(f"Found {len(result['history'])} records")
                        st.dataframe(
                            pd.DataFrame(result['history']),
                            use_container_width=True
                        )
                    else:
                        st.warning(f"No history found for breaker {breaker_id}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a breaker ID")


# ─────────────────────────────────────
# PAGE 3 - ABOUT
# ─────────────────────────────────────
elif page == "About":
    st.header("About")
    
    st.markdown("""
    ### DCRM Anomaly Detection System
    
    This system detects faults in **Extra High Voltage (EHV) Circuit Breakers**
    using Dynamic Contact Resistance Measurement (DCRM) test data.
    
    ---
    
    ### How it works
    - Upload a DCRM test CSV file
    - System preprocesses and analyzes the data
    - Isolation Forest model detects anomalies
    - SHAP values identify faulty components
    - Maintenance recommendations are generated
    
    ---
    
    ### Model Performance
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Detection Rate", "82.4%")
    col2.metric("False Alarm Rate", "22.1%")
    col3.metric("Contamination", "0.22")
    
    st.markdown("""
    ---
    ### Tech Stack
    - **ML Model:** Isolation Forest
    - **Explainability:** SHAP
    - **Backend:** FastAPI
    - **Frontend:** Streamlit
    - **Data:** Proprietary DCRM Dataset
    """)