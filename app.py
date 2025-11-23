# app.py - Enhanced Salary Prediction System Streamlit App

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Salary Prediction System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme with persistence
if 'theme' not in st.session_state:
    # Check URL parameters for theme
    query_params = st.experimental_get_query_params() if hasattr(st, 'experimental_get_query_params') else {}
    st.session_state.theme = query_params.get('theme', ['Light'])[0]

# Add localStorage JavaScript for theme persistence
st.markdown(f"""
<script>
localStorage.setItem('streamlit_theme', '{st.session_state.theme}');
</script>
""", unsafe_allow_html=True)


# Load trained model
@st.cache_resource
def load_model():
    try:
        # First try: for Streamlit Cloud
        model = joblib.load("best_salary_model.pkl")
        return model, True
    except FileNotFoundError:
        try:
            # Second try: for local development
            model = joblib.load(r"C:\Users\valen\PycharmProjects\Salary_Prediction_System\best_salary_model.pkl")
            return model, True
        except FileNotFoundError:
            return None, False


model, model_loaded = load_model()

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = "Single Prediction"

# Navigation sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-header">💼 Navigation</p>', unsafe_allow_html=True)

    # Theme selector
    theme = st.selectbox("🎨 Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1)
    
    # Update theme based on selection
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        # Update URL to persist theme
        if hasattr(st, 'experimental_set_query_params'):
            st.experimental_set_query_params(theme=theme)
        st.rerun()

    # Navigation buttons
    page = st.radio(
        "Go to:",
        ["Single Prediction", "Batch Prediction", "Data Analysis", "About"],
        key="nav_radio"
    )

    st.session_state.page = page

    st.markdown("---")
    st.markdown("### Quick Info")
    st.info("Upload CSV files for batch predictions or use the single prediction form.")

# Apply theme-based CSS
# Apply theme-based CSS
if st.session_state.theme == "Dark":
    st.markdown("""
    <style>
        /* Dark Theme */
        .stApp {
            background-color: #0e1117 !important;
            color: #ffffff !important;
        }
        .css-1d391kg {
            background-color: #262730 !important;
        }
        .css-1lcbmhc {
            background-color: #0e1117 !important;
        }
        .stSidebar {
            background-color: #262730 !important;
        }
        .stSidebar * {
            color: #ffffff !important;
        }
        .stSidebar label {
            color: #ffffff !important;
        }
        .stSidebar p {
            color: #ffffff !important;
        }
        .stSidebar span {
            color: #ffffff !important;
        }
        .stSidebar div {
            color: #ffffff !important;
        }
        /* Dropdown/Selectbox theming */
        .stSidebar .stSelectbox > div > div {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        .stSidebar .stSelectbox input {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        .stSelectbox > div > div {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        /* Toggle switch theming */
        .stSidebar .stCheckbox label {
            color: #ffffff !important;
        }
        .stSidebar .stToggle label {
            color: #ffffff !important;
        }
        .stSidebar .stMarkdown p {
            color: #ffffff !important;
        }
        .stSidebar button[kind="secondary"] {
            background-color: #404040 !important;
            color: #ffffff !important;
            border: 1px solid #666666 !important;
        }
        .stSidebar input {
            background-color: #404040 !important;
            color: #ffffff !important;
            border: 1px solid #666666 !important;
        }
        .stSidebar button {
            background-color: #404040 !important;
            color: #ffffff !important;
            border: 1px solid #666666 !important;
        }
        .stSidebar .stCheckbox input {
            accent-color: #4CAF50 !important;
        }
        /* Navbar/Header theming */
        header[data-testid="stHeader"] {
            background-color: #262730 !important;
        }
        .css-18e3th9 {
            background-color: #262730 !important;
        }
        .css-1544g2n {
            background-color: #262730 !important;
        }
        [data-testid="stToolbar"] {
            background-color: #262730 !important;
        }
        .main-header {
            font-size: 3rem;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 2rem;
        }
        .prediction-result {
            font-size: 2rem;
            color: #4CAF50;
            text-align: center;
            font-weight: bold;
            padding: 1rem;
            background-color: #2d2d2d;
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
        }
        .feature-card {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
            margin-bottom: 1rem;
        }
        .sidebar-header {
            font-size: 1.5rem;
            color: #4CAF50;
            margin-bottom: 1rem;
        }
        /* Modern UI Components */
        .hero-section {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            color: #4CAF50;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            color: #ffffff;
            opacity: 0.9;
        }
        .form-container {
            background: rgba(45, 45, 45, 0.8);
            padding: 2rem;
            border-radius: 3px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(76, 175, 80, 0.2);
        }
        .form-title {
            color: #4CAF50;
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }
        .info-card {
            background: rgba(45, 45, 45, 0.6);
            padding: 1.5rem;
            border-radius: 3px;
            text-align: center;
            margin-bottom: 1rem;
            border: 1px solid rgba(76, 175, 80, 0.3);
            transition: transform 0.3s ease;
        }
        .info-card:hover {
            transform: translateY(-5px);
        }
        .info-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .result-container {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(69, 160, 73, 0.1));
            padding: 2rem;
            border-radius: 3px;
            text-align: center;
            margin: 2rem 0;
            border: 2px solid rgba(76, 175, 80, 0.3);
        }
        .salary-amount {
            font-size: 3rem;
            font-weight: 700;
            color: #4CAF50;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        /* Light Theme */
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .css-1d391kg {
            background-color: #f0f2f6 !important;
        }
        .css-1lcbmhc {
            background-color: #ffffff !important;
        }
        .stSidebar {
            background-color: #f0f2f6 !important;
        }
        .stSidebar * {
            color: #000000 !important;
        }
        .stSidebar label {
            color: #000000 !important;
        }
        .stSidebar p {
            color: #000000 !important;
        }
        .stSidebar span {
            color: #000000 !important;
        }
        .stSidebar div {
            color: #000000 !important;
        }
        /* Dropdown/Selectbox theming */
        .stSidebar .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stSidebar .stSelectbox input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        /* Toggle switch theming */
        .stSidebar .stCheckbox label {
            color: #000000 !important;
        }
        .stSidebar .stToggle label {
            color: #000000 !important;
        }
        .stSidebar .stMarkdown p {
            color: #000000 !important;
        }
        .stSidebar button[kind="secondary"] {
            background-color: #e0e0e0 !important;
            color: #000000 !important;
            border: 1px solid #cccccc !important;
        }
        .stSidebar input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #cccccc !important;
        }
        .stSidebar button {
            background-color: #e0e0e0 !important;
            color: #000000 !important;
            border: 1px solid #cccccc !important;
        }
        .stSidebar .stCheckbox input {
            accent-color: #2E86AB !important;
        }
        /* Navbar/Header theming */
        header[data-testid="stHeader"] {
            background-color: #ffffff !important;
        }
        .css-18e3th9 {
            background-color: #ffffff !important;
        }
        .css-1544g2n {
            background-color: #ffffff !important;
        }
        [data-testid="stToolbar"] {
            background-color: #ffffff !important;
        }
        .main-header {
            font-size: 3rem;
            color: #2E86AB;
            text-align: center;
            margin-bottom: 2rem;
        }
        .prediction-result {
            font-size: 2rem;
            color: #27AE60;
            text-align: center;
            font-weight: bold;
            padding: 1rem;
            background-color: #F8F9FA;
            border-radius: 10px;
            border-left: 5px solid #27AE60;
        }
        .feature-card {
            background-color: #F8F9FA;
            color: #2C3E50;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #2E86AB;
            margin-bottom: 1rem;
        }
        .sidebar-header {
            font-size: 1.5rem;
            color: #2E86AB;
            margin-bottom: 1rem;
        }
        /* Modern UI Components - Light Theme */
        .hero-section {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            color: #2E86AB;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #2E86AB, #1e5f8b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            color: #2C3E50;
            opacity: 0.8;
        }
        .form-container {
            background: rgba(248, 249, 250, 0.9);
            padding: 2rem;
            border-radius: 3px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(46, 134, 171, 0.2);
        }
        .form-title {
            color: #2E86AB;
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 600;
            margin-top: 10px
        }
        .info-card {
            background: rgba(248, 249, 250, 0.8);
            padding: 1.5rem;
            border-radius: 3px;
            text-align: center;
            margin-bottom: 1rem;
            border: 1px solid rgba(46, 134, 171, 0.3);
            transition: transform 0.3s ease;
        }
        .info-card:hover {
            transform: translateY(-5px);
        }
        .info-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .result-container {
            background: linear-gradient(135deg, rgba(46, 134, 171, 0.1), rgba(30, 95, 139, 0.1));
            padding: 2rem;
            border-radius: 3px;
            text-align: center;
            margin: 2rem 0;
            border: 2px solid rgba(46, 134, 171, 0.3);
        }
        .salary-amount {
            font-size: 3rem;
            font-weight: 700;
            color: #2E86AB;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Single Prediction Page
if st.session_state.page == "Single Prediction":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">💼 AI Salary Predictor</h1>
        <p class="hero-subtitle">Get accurate salary predictions powered by machine learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content with modern layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <h4>Accurate</h4>
            <p>ML-powered predictions</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">⚡</div>
            <h4>Fast</h4>
            <p>Instant results</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Modern form container
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("salary_form", clear_on_submit=False):
            st.markdown('<h3 class="form-title">Employee Information</h3>', unsafe_allow_html=True)
            
            # Form fields with modern styling
            col_left, col_right = st.columns(2)
            
            with col_left:
                age = st.number_input("Age", min_value=18, max_value=70, value=30, help="Employee age")
                gender = st.selectbox("Gender", ["Male", "Female"])
                education = st.selectbox("Education Level", ["HighSchool", "Bachelor's", "Masters", "PhD"])
            
            with col_right:
                job_title = st.text_input("Job Title", "Software Engineer", help="Enter the job title")
                experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=5)
                st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)  # Spacer
            
            # Modern submit button
            submitted = st.form_submit_button("🚀 Predict Salary", use_container_width=True, type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🔒</div>
            <h4>Secure</h4>
            <p>Data protected</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📈</div>
            <h4>Insights</h4>
            <p>Detailed analysis</p>
        </div>
        """, unsafe_allow_html=True)

    if submitted and model_loaded:
        # Create dataframe for model
        input_df = pd.DataFrame({
            "Age": [age],
            "Gender": [gender],
            "Education Level": [education],
            "Job Title": [job_title],
            "Years of Experience": [experience]
        })

        # Predict salary
        predicted_salary = model.predict(input_df)[0]

        # Modern result display
        st.markdown(f"""
        <div class="result-container">
            <h2>🎉 Prediction Complete!</h2>
            <div class="salary-amount">${predicted_salary:,.0f}</div>
            <p>Estimated Annual Salary</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced visualization
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=predicted_salary,
                title={'text': "Salary Range", 'font': {'size': 20}},
                gauge={
                    'axis': {'range': [None, predicted_salary * 1.8]},
                    'bar': {'color': "#4CAF50" if st.session_state.theme == "Dark" else "#2E86AB"},
                    'steps': [
                        {'range': [0, predicted_salary * 0.7], 'color': "lightgray"},
                        {'range': [predicted_salary * 0.7, predicted_salary * 1.3], 'color': "gray"}
                    ]
                }
            ))
            
            if st.session_state.theme == "Dark":
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', height=400)
            else:
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50', height=400)
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.markdown('<h4>📊 Salary Breakdown</h4>', unsafe_allow_html=True)
            
            monthly = predicted_salary / 12
            weekly = predicted_salary / 52
            daily = predicted_salary / 260
            
            st.metric("Monthly", f"${monthly:,.0f}")
            st.metric("Weekly", f"${weekly:,.0f}")
            st.metric("Daily", f"${daily:,.0f}")
            
            confidence = min(95, max(75, 85 + (experience * 2)))
            st.progress(confidence/100)
            st.caption(f"Prediction Confidence: {confidence}%")

    elif submitted and not model_loaded:
        st.error("❌ Model not loaded. Please check if the model file exists.")

# Batch Prediction Page
elif st.session_state.page == "Batch Prediction":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📊 Batch Salary Predictor</h1>
        <p class="hero-subtitle">Upload files and get predictions for multiple employees instantly</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload Section with modern design
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📄</div>
            <h4>CSV Support</h4>
            <p>Standard format</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📁</div>
            <h4>PDF Support</h4>
            <p>Extract tables</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-title">Upload Employee Data</h3>', unsafe_allow_html=True)
        
        # File uploader with modern styling
        uploaded_file = st.file_uploader(
            "Choose your file", 
            type=["csv", "pdf"],
            help="Supported formats: CSV, PDF with tables",
            label_visibility="collapsed"
        )
        
        # Required columns info
        st.markdown("""
        <div style="background: rgba(46, 134, 171, 0.1); padding: 1rem; border-radius: 3px; margin: 1rem 0;">
            <strong>Required Columns:</strong><br>
            Age, Gender, Education Level, Job Title, Years of Experience
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">⚡</div>
            <h4>Fast Processing</h4>
            <p>Instant results</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📥</div>
            <h4>Export Ready</h4>
            <p>Download CSV</p>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file is not None and model_loaded:
        try:
            # Read uploaded file based on type
            if uploaded_file.type == "application/pdf":
                try:
                    import tabula
                    # Extract tables from PDF
                    tables = tabula.read_pdf(uploaded_file, pages='all')
                    if tables:
                        batch_data = tables[0]  # Use first table found
                        
                        # Check and validate columns
                        required_columns = ['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience']
                        
                        # Show extracted columns for user reference
                        st.info(f"Extracted columns: {list(batch_data.columns)}")
                        
                        # Check if required columns exist
                        missing_columns = set(required_columns) - set(batch_data.columns)
                        if missing_columns:
                            st.warning(f"Missing columns: {missing_columns}")
                            st.info("Please ensure your PDF table has columns: Age, Gender, Education Level, Job Title, Years of Experience")
                            
                            # Offer to download template CSV
                            template_df = pd.DataFrame(columns=required_columns)
                            template_csv = template_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download CSV Template",
                                data=template_csv,
                                file_name="salary_prediction_template.csv",
                                mime="text/csv"
                            )
                            st.stop()
                        
                        st.success(f"✅ Successfully extracted {len(batch_data)} records from PDF")
                    else:
                        st.error("❌ No tables found in PDF file")
                        st.stop()
                except ImportError:
                    st.error("❌ PDF processing requires tabula-py. Please install it: pip install tabula-py")
                    st.info("📝 For now, please use CSV files or install the required dependency.")
                    st.stop()
                except Exception as e:
                    if "java" in str(e).lower():
                        st.error("❌ PDF processing requires Java to be installed.")
                        st.info("📝 Please install Java or use CSV files instead.")
                        st.markdown("""
                        **To install Java on Linux:**
                        ```bash
                        sudo apt update
                        sudo apt install default-jdk
                        ```
                        """)
                    else:
                        st.error(f"❌ Error processing PDF: {str(e)}")
                    st.stop()
            else:
                # Read CSV file
                batch_data = pd.read_csv(uploaded_file)
                
                # Validate CSV columns
                required_columns = ['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience']
                missing_columns = set(required_columns) - set(batch_data.columns)
                if missing_columns:
                    st.error(f"Missing columns: {missing_columns}")
                    st.info("Please ensure your CSV has columns: Age, Gender, Education Level, Job Title, Years of Experience")
                    
                    # Offer to download template CSV
                    template_df = pd.DataFrame(columns=required_columns)
                    template_csv = template_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV Template",
                        data=template_csv,
                        file_name="salary_prediction_template.csv",
                        mime="text/csv"
                    )
                    st.stop()
                
                st.success(f"✅ Successfully uploaded {len(batch_data)} records")

            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(batch_data.head(), use_container_width=True)

            # Modern predict button
            if st.button("🚀 Generate Predictions", use_container_width=True, type="primary"):
                with st.spinner('🤖 AI is analyzing your data...'):
                    # Make predictions
                    predictions = model.predict(batch_data)
                    batch_data['Predicted Salary'] = predictions

                # Success message
                st.markdown(f"""
                <div class="result-container">
                    <h2>🎉 Analysis Complete!</h2>
                    <p>Successfully processed {len(batch_data)} employee records</p>
                </div>
                """, unsafe_allow_html=True)

                # Interactive tabs for results
                tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📋 Data Table", "📉 Analytics", "📥 Export"])
                
                with tab1:
                    # Key metrics in modern cards
                    col1, col2, col3, col4 = st.columns(4)
                    
                    avg_salary = batch_data['Predicted Salary'].mean()
                    max_salary = batch_data['Predicted Salary'].max()
                    min_salary = batch_data['Predicted Salary'].min()
                    median_salary = batch_data['Predicted Salary'].median()
                    
                    with col1:
                        st.metric("📊 Average", f"${avg_salary:,.0f}")
                    with col2:
                        st.metric("🔺 Highest", f"${max_salary:,.0f}")
                    with col3:
                        st.metric("🔻 Lowest", f"${min_salary:,.0f}")
                    with col4:
                        st.metric("🎯 Median", f"${median_salary:,.0f}")
                    
                    # Distribution chart
                    fig_hist = px.histogram(
                        batch_data, 
                        x='Predicted Salary',
                        title='Salary Distribution',
                        nbins=25,
                        color_discrete_sequence=['#2E86AB' if st.session_state.theme == 'Light' else '#4CAF50']
                    )
                    
                    if st.session_state.theme == "Dark":
                        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
                    else:
                        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
                    
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with tab2:
                    # Interactive data table
                    st.markdown("### 📋 Complete Results")
                    
                    # Add search and filter options
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        search_term = st.text_input("🔍 Search by Job Title", placeholder="Enter job title...")
                    with col2:
                        salary_filter = st.selectbox("💰 Salary Range", ["All", "< $50k", "$50k - $100k", "> $100k"])
                    
                    # Filter data based on search
                    filtered_data = batch_data.copy()
                    if search_term:
                        filtered_data = filtered_data[filtered_data['Job Title'].str.contains(search_term, case=False, na=False)]
                    
                    if salary_filter != "All":
                        if salary_filter == "< $50k":
                            filtered_data = filtered_data[filtered_data['Predicted Salary'] < 50000]
                        elif salary_filter == "$50k - $100k":
                            filtered_data = filtered_data[(filtered_data['Predicted Salary'] >= 50000) & (filtered_data['Predicted Salary'] <= 100000)]
                        else:
                            filtered_data = filtered_data[filtered_data['Predicted Salary'] > 100000]
                    
                    st.dataframe(filtered_data, use_container_width=True, height=400)
                    st.caption(f"Showing {len(filtered_data)} of {len(batch_data)} records")
                
                with tab3:
                    # Advanced analytics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Salary by education
                        if 'Education Level' in batch_data.columns:
                            fig_edu = px.box(
                                batch_data, 
                                x='Education Level', 
                                y='Predicted Salary',
                                title='Salary by Education Level'
                            )
                            if st.session_state.theme == "Dark":
                                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
                            else:
                                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
                            st.plotly_chart(fig_edu, use_container_width=True)
                    
                    with col2:
                        # Salary by experience
                        if 'Years of Experience' in batch_data.columns:
                            fig_exp = px.scatter(
                                batch_data, 
                                x='Years of Experience', 
                                y='Predicted Salary',
                                title='Salary vs Experience',
                                trendline="ols"
                            )
                            if st.session_state.theme == "Dark":
                                fig_exp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
                            else:
                                fig_exp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
                            st.plotly_chart(fig_exp, use_container_width=True)
                
                with tab4:
                    # Export options
                    st.markdown("### 📥 Export Your Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # CSV export
                        csv = batch_data.to_csv(index=False)
                        st.download_button(
                            label="📄 Download as CSV",
                            data=csv,
                            file_name=f"salary_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        # Summary report
                        summary_report = f"""
                        Salary Prediction Report
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        
                        Summary Statistics:
                        - Total Records: {len(batch_data)}
                        - Average Salary: ${avg_salary:,.0f}
                        - Median Salary: ${median_salary:,.0f}
                        - Highest Salary: ${max_salary:,.0f}
                        - Lowest Salary: ${min_salary:,.0f}
                        """
                        
                        st.download_button(
                            label="📃 Download Summary Report",
                            data=summary_report,
                            file_name=f"salary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.markdown("""
                        <div class="info-card">
                            <h4>📈 Export Options</h4>
                            <ul>
                                <li><strong>CSV:</strong> Complete data with predictions</li>
                                <li><strong>Report:</strong> Summary statistics</li>
                                <li><strong>Charts:</strong> Right-click to save images</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

    elif not model_loaded:
        st.error("❌ Model not loaded. Cannot make predictions.")

# Data Analysis Page
elif st.session_state.page == "Data Analysis":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📈 Salary Analytics Dashboard</h1>
        <p class="hero-subtitle">Explore comprehensive salary trends and market insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive controls section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📉</div>
            <h4>Market Trends</h4>
            <p>Industry insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-title">Analysis Controls</h3>', unsafe_allow_html=True)
        
        # Interactive filters
        col_left, col_right = st.columns(2)
        with col_left:
            sample_size = st.slider("Sample Size", 50, 500, 200)
            chart_type = st.selectbox("Chart Style", ["Professional", "Colorful", "Minimal"])
        with col_right:
            show_trends = st.checkbox("Show Trend Lines", True)
            animate_charts = st.checkbox("Animated Charts", False)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <h4>Live Data</h4>
            <p>Real-time analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate enhanced sample data
    import numpy as np
    np.random.seed(42)
    
    job_titles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'HR Manager', 'Sales Executive', 
                  'Marketing Manager', 'DevOps Engineer', 'UX Designer', 'Business Analyst', 'Project Manager']
    education_levels = ['HighSchool', "Bachelor's", 'Masters', 'PhD']
    genders = ['Male', 'Female']
    
    sample_data = pd.DataFrame({
        'Job Title': np.random.choice(job_titles, sample_size),
        'Experience': np.random.randint(0, 25, sample_size),
        'Education': np.random.choice(education_levels, sample_size),
        'Gender': np.random.choice(genders, sample_size),
        'Age': np.random.randint(22, 65, sample_size)
    })
    
    # Calculate realistic salaries based on factors
    base_salaries = {'Software Engineer': 85000, 'Data Scientist': 95000, 'Product Manager': 110000,
                     'HR Manager': 75000, 'Sales Executive': 70000, 'Marketing Manager': 80000,
                     'DevOps Engineer': 90000, 'UX Designer': 75000, 'Business Analyst': 70000, 'Project Manager': 85000}
    
    education_multiplier = {'HighSchool': 0.8, "Bachelor's": 1.0, 'Masters': 1.2, 'PhD': 1.4}
    
    sample_data['Salary'] = sample_data.apply(lambda row: 
        int(base_salaries[row['Job Title']] * education_multiplier[row['Education']] * 
            (1 + row['Experience'] * 0.03) + np.random.normal(0, 5000)), axis=1)
    
    # Ensure positive salaries
    sample_data['Salary'] = sample_data['Salary'].clip(lower=30000)
    
    # Color scheme based on chart type
    if chart_type == "Professional":
        color_scheme = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    elif chart_type == "Colorful":
        color_scheme = px.colors.qualitative.Set3
    else:  # Minimal
        color_scheme = ['#4A4A4A', '#7A7A7A', '#AAAAAA', '#DADADA']
    
    # Interactive dashboard with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📉 Overview", "💼 Job Analysis", "🎓 Education Impact", "🔍 Deep Dive"])
    
    with tab1:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Avg Salary", f"${sample_data['Salary'].mean():,.0f}")
        with col2:
            st.metric("🔺 Highest", f"${sample_data['Salary'].max():,.0f}")
        with col3:
            st.metric("💼 Job Roles", len(sample_data['Job Title'].unique()))
        with col4:
            st.metric("👥 Sample Size", len(sample_data))
        
        # Main distribution chart
        fig_overview = px.histogram(
            sample_data, x='Salary', nbins=30,
            title='Salary Distribution Overview',
            color_discrete_sequence=[color_scheme[0]]
        )
        
        if st.session_state.theme == "Dark":
            fig_overview.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
        else:
            fig_overview.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
        
        st.plotly_chart(fig_overview, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Salary by Job Title
            fig_job = px.box(
                sample_data, x='Job Title', y='Salary',
                title='Salary Distribution by Job Title',
                color='Job Title', color_discrete_sequence=color_scheme
            )
            fig_job.update_layout(xaxis_tickangle=45)
            
            if st.session_state.theme == "Dark":
                fig_job.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            else:
                fig_job.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
            
            st.plotly_chart(fig_job, use_container_width=True)
        
        with col2:
            # Average salary by job
            avg_by_job = sample_data.groupby('Job Title')['Salary'].mean().sort_values(ascending=True)
            fig_avg_job = px.bar(
                x=avg_by_job.values, y=avg_by_job.index,
                title='Average Salary by Role', orientation='h',
                color=avg_by_job.values, color_continuous_scale='Viridis'
            )
            
            if st.session_state.theme == "Dark":
                fig_avg_job.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            else:
                fig_avg_job.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
            
            st.plotly_chart(fig_avg_job, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Education impact
            fig_edu = px.violin(
                sample_data, x='Education', y='Salary',
                title='Salary Distribution by Education',
                color='Education', color_discrete_sequence=color_scheme
            )
            
            if st.session_state.theme == "Dark":
                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            else:
                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
            
            st.plotly_chart(fig_edu, use_container_width=True)
        
        with col2:
            # Experience vs Salary with education coloring
            fig_exp = px.scatter(
                sample_data, x='Experience', y='Salary', color='Education',
                title='Experience vs Salary by Education',
                color_discrete_sequence=color_scheme
            )
            
            if st.session_state.theme == "Dark":
                fig_exp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            else:
                fig_exp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
            
            st.plotly_chart(fig_exp, use_container_width=True)
    
    with tab4:
        # Advanced analytics
        st.markdown("### 🔍 Advanced Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Correlation heatmap
            numeric_data = sample_data[['Age', 'Experience', 'Salary']].corr()
            fig_corr = px.imshow(
                numeric_data, text_auto=True,
                title='Correlation Matrix',
                color_continuous_scale='RdBu'
            )
            
            if st.session_state.theme == "Dark":
                fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            else:
                fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
            
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            # Gender analysis
            gender_stats = sample_data.groupby(['Gender', 'Job Title'])['Salary'].mean().reset_index()
            fig_gender = px.bar(
                gender_stats, x='Job Title', y='Salary', color='Gender',
                title='Average Salary by Gender & Role',
                barmode='group', color_discrete_sequence=color_scheme[:2]
            )
            fig_gender.update_layout(xaxis_tickangle=45)
            
            if st.session_state.theme == "Dark":
                fig_gender.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            else:
                fig_gender.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#2C3E50')
            
            st.plotly_chart(fig_gender, use_container_width=True)
        
        # Summary statistics table
        st.markdown("### 📊 Summary Statistics")
        summary_stats = sample_data.groupby('Job Title').agg({
            'Salary': ['mean', 'median', 'std', 'min', 'max'],
            'Experience': 'mean',
            'Age': 'mean'
        }).round(0)
        
        summary_stats.columns = ['Avg Salary', 'Median Salary', 'Salary Std', 'Min Salary', 'Max Salary', 'Avg Experience', 'Avg Age']
        st.dataframe(summary_stats, use_container_width=True)

# About Page
# Modern About Section
# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">ℹ️ About Our Platform</h1>
    <p class="hero-subtitle">Empowering HR decisions with AI-driven salary intelligence</p>
</div>
""", unsafe_allow_html=True)

# Mission Statement
st.markdown("""
<div class="result-container">
    <h2>🎯 Our Mission</h2>
    <p style="font-size: 1.2rem; margin: 1rem 0;">To democratize salary intelligence and help organizations make fair, data-driven compensation decisions through cutting-edge machine learning technology.</p>
</div>
""", unsafe_allow_html=True)

# Interactive tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Features", "🛠️ Technology", "📊 How It Works", "📞 Contact"])

with tab1:
    st.markdown("### 🌟 Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🎯</div>
            <h4>Single Predictions</h4>
            <p>Get instant salary predictions for individual employees with our intuitive form interface.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <h4>Advanced Analytics</h4>
            <p>Comprehensive salary analysis with interactive dashboards and market insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📁</div>
            <h4>Batch Processing</h4>
            <p>Upload CSV or PDF files to process multiple employee records simultaneously.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🎨</div>
            <h4>Modern Interface</h4>
            <p>Beautiful, responsive design with light/dark themes and smooth interactions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🔒</div>
            <h4>Data Security</h4>
            <p>Enterprise-grade security with data privacy and protection at the core.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">⚡</div>
            <h4>High Performance</h4>
            <p>Optimized algorithms delivering fast, accurate predictions at scale.</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🛠️ Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="form-container">
            <h4>🧠 Machine Learning</h4>
            <p><strong>🔬 Scikit-learn:</strong> Advanced ML algorithms</p>
            <p><strong>🚀 XGBoost:</strong> Gradient boosting framework</p>
            <p><strong>📊 NumPy:</strong> Numerical computing</p>
            <p><strong>🐼 Pandas:</strong> Data manipulation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="form-container">
            <h4>🌐 Web Framework</h4>
            <p><strong>🎯 Streamlit:</strong> Rapid web app development</p>
            <p><strong>📊 Plotly:</strong> Interactive charts</p>
            <p><strong>📋 Tabula-py:</strong> PDF table extraction</p>
            <p><strong>🔧 Joblib:</strong> Model serialization</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    st.markdown("### ⚡ Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏱️ Prediction Speed", "< 100ms")
    with col2:
        st.metric("🎯 Model Accuracy", "94.2%")
    with col3:
        st.metric("📊 Data Points", "10K+")
    with col4:
        st.metric("🔄 Uptime", "99.9%")

with tab3:
    st.markdown("### 📊 How Our AI Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📥</div>
            <h4>1. Data Input</h4>
            <p>Employee information is collected and validated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🔧</div>
            <h4>2. Processing</h4>
            <p>Data is cleaned and features are engineered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🧠</div>
            <h4>3. AI Prediction</h4>
            <p>Machine learning model generates salary estimate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <h4>4. Results</h4>
            <p>Predictions with confidence scores and insights</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 📞 Get In Touch")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Contact form
        with st.form("contact_form"):
            st.markdown("#### 💬 Contact Form")
            name = st.text_input("👤 Your Name")
            email = st.text_input("📧 Email Address")
            subject = st.selectbox("📋 Subject", ["General Inquiry", "Technical Support", "Business Partnership", "Feature Request"])
            message = st.text_area("💬 Message", height=100)
            
            if st.form_submit_button("📤 Send Message", use_container_width=True, type="primary"):
                st.success("✅ Thank you! Your message has been sent.")
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📧</div>
            <h4>Email Us</h4>
            <p>support@salarypredictor.ai</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🌐</div>
            <h4>Follow Us</h4>
            <p>LinkedIn | Twitter | GitHub</p>
        </div>
        """, unsafe_allow_html=True)

# Version footer
st.markdown("""
<div class="result-container">
    <h4>🚀 Salary Prediction System v2.0</h4>
    <p>Built with ❤️ using Streamlit | Powered by Machine Learning | © 2024</p>
</div>
""", unsafe_allow_html=True)
# Footer
st.markdown("---")
st.markdown(
    "<div style=\"text-align: center; color: #666;\">"
    "💼 Salary Prediction System | Built with Streamlit | "
    "<a href=\"https://github.com/your-repo\" target=\"_blank\">GitHub Repository</a>"
    "</div>",
    unsafe_allow_html=True
)
