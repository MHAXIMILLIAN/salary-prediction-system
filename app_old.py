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

    # Theme toggle switch
    st.markdown("🎨 **Theme**")
    dark_mode = st.toggle("Dark Mode", value=st.session_state.theme == "Dark")
    
    # Update theme based on toggle
    new_theme = "Dark" if dark_mode else "Light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        # Update URL to persist theme
        if hasattr(st, 'experimental_set_query_params'):
            st.experimental_set_query_params(theme=new_theme)
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
        .stSidebar .stCheckbox input[type="checkbox"] {
            background-color: #000000 !important;
            border: 2px solid #000000 !important;
        }
        .stSidebar button[data-testid] {
            background-color: #000000 !important;
            color: #ffffff !important;
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
    </style>
    """, unsafe_allow_html=True)

# Single Prediction Page
if st.session_state.page == "Single Prediction":
    st.markdown('<h1 class="main-header">💼 Salary Prediction System</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🔮 Predict Employee Salaries Accurately</h3>
        <p>This advanced machine learning system predicts salaries based on multiple factors including demographics, education, job role, and professional experience.</p>
        </div>
        """, unsafe_allow_html=True)

        # Prediction form in main area
        with st.form("salary_form"):
            st.subheader("📋 Employee Details")

            col1_form, col2_form = st.columns(2)

            with col1_form:
                age = st.number_input("🎂 Age", min_value=18, max_value=70, value=30, help="Employee age")
                gender = st.selectbox("🚻 Gender", ["Male", "Female"])
                education = st.selectbox("🎓 Education Level", ["HighSchool", "Bachelor's", "Masters", "PhD"])

            with col2_form:
                job_title = st.text_input("💼 Job Title", "Software Engineer", help="Enter the job title")
                experience = st.number_input("📈 Years of Experience", min_value=0, max_value=50, value=5)

            submitted = st.form_submit_button("🚀 Predict Salary", use_container_width=True)

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135707.png", width=150)
        st.markdown("""
        <div class="feature-card">
        <h4>📊 Features</h4>
        <ul>
        <li>Single & Batch Predictions</li>
        <li>Data Visualization</li>
        <li>Export Results</li>
        <li>Theme Customization</li>
        </ul>
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

        # Display result
        st.markdown(f'<p class="prediction-result">💰 Predicted Salary: ${predicted_salary:,.0f}</p>',
                    unsafe_allow_html=True)

        # Visualization
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=predicted_salary,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Predicted Salary"},
            gauge={
                'axis': {'range': [None, predicted_salary * 1.5]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, predicted_salary * 0.5], 'color': "lightgray"},
                    {'range': [predicted_salary * 0.5, predicted_salary], 'color': "gray"}
                ]
            }
        ))
        
        # Apply theme to chart
        if st.session_state.theme == "Dark":
            fig.update_layout(
                paper_bgcolor='#1e1e1e',
                plot_bgcolor='#1e1e1e',
                font_color='#ffffff'
            )
        else:
            fig.update_layout(
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                font_color='#2C3E50'
            )
        
        st.plotly_chart(fig, use_container_width=True)

    elif submitted and not model_loaded:
        st.error("❌ Model not loaded. Please check if the model file exists.")

# Batch Prediction Page
elif st.session_state.page == "Batch Prediction":
    st.markdown('<h1 class="main-header">📊 Batch Prediction</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
    <h3>📁 Upload CSV File for Multiple Predictions</h3>
    <p>Upload a CSV file containing employee data to get salary predictions for multiple employees at once.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv",
                                     help="CSV should have columns: Age, Gender, Education Level, Job Title, Years of Experience")

    if uploaded_file is not None and model_loaded:
        try:
            # Read uploaded file
            batch_data = pd.read_csv(uploaded_file)
            st.success(f"✅ Successfully uploaded {len(batch_data)} records")

            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(batch_data.head(), use_container_width=True)

            if st.button("🔮 Predict All Salaries", use_container_width=True):
                # Make predictions
                predictions = model.predict(batch_data)
                batch_data['Predicted Salary'] = predictions

                # Display results
                st.subheader("📈 Prediction Results")
                st.dataframe(batch_data, use_container_width=True)

                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Salary", f"${batch_data['Predicted Salary'].mean():,.0f}")
                with col2:
                    st.metric("Highest Salary", f"${batch_data['Predicted Salary'].max():,.0f}")
                with col3:
                    st.metric("Lowest Salary", f"${batch_data['Predicted Salary'].min():,.0f}")

                # Visualization
                fig = px.histogram(batch_data, x='Predicted Salary',
                                   title='Distribution of Predicted Salaries',
                                   nbins=20)
                
                # Apply theme to chart
                if st.session_state.theme == "Dark":
                    fig.update_layout(
                        paper_bgcolor='#1e1e1e',
                        plot_bgcolor='#1e1e1e',
                        font_color='#ffffff'
                    )
                else:
                    fig.update_layout(
                        paper_bgcolor='#ffffff',
                        plot_bgcolor='#ffffff',
                        font_color='#2C3E50'
                    )
                
                st.plotly_chart(fig, use_container_width=True)

                # Export functionality
                st.subheader("💾 Export Results")
                csv = batch_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Predictions as CSV",
                    data=csv,
                    file_name=f"salary_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

    elif not model_loaded:
        st.error("❌ Model not loaded. Cannot make predictions.")

# Data Analysis Page
elif st.session_state.page == "Data Analysis":
    st.markdown('<h1 class="main-header">📈 Data Analysis</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
    <h3>📊 Salary Distribution Analysis</h3>
    <p>Explore salary distributions and patterns across different demographics and job roles.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sample data for demonstration (replace with your actual data patterns)
    sample_data = pd.DataFrame({
        'Job Title': ['Software Engineer', 'Data Scientist', 'Product Manager', 'HR Manager', 'Sales Executive'] * 20,
        'Experience': list(range(1, 11)) * 10,
        'Education': ['Bachelor\'s', 'Masters', 'PhD', 'Bachelor\'s', 'Masters'] * 20,
        'Salary': [80000 + i * 5000 + j * 3000 for i in range(100) for j in range(1)][:100]
    })

    # Visualization 1: Salary by Job Title
    fig1 = px.box(sample_data, x='Job Title', y='Salary',
                  title='Salary Distribution by Job Title')
    if st.session_state.theme == "Dark":
        fig1.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font_color='#ffffff'
        )
    else:
        fig1.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font_color='#2C3E50'
        )
    st.plotly_chart(fig1, use_container_width=True)

    # Visualization 2: Salary vs Experience
    fig2 = px.scatter(sample_data, x='Experience', y='Salary', color='Education',
                      title='Salary vs Years of Experience by Education Level')
    if st.session_state.theme == "Dark":
        fig2.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font_color='#ffffff'
        )
    else:
        fig2.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font_color='#2C3E50'
        )
    st.plotly_chart(fig2, use_container_width=True)

    # Visualization 3: Average Salary by Education
    avg_salary = sample_data.groupby('Education')['Salary'].mean().reset_index()
    fig3 = px.bar(avg_salary, x='Education', y='Salary',
                  title='Average Salary by Education Level')
    if st.session_state.theme == "Dark":
        fig3.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font_color='#ffffff'
        )
    else:
        fig3.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font_color='#2C3E50'
        )
    st.plotly_chart(fig3, use_container_width=True)

# About Page
else:
    st.markdown('<h1 class="main-header">ℹ️ About</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>About Salary Prediction System</h3>
        <p>This is an advanced machine learning application designed to predict employee salaries based on various features including demographics, education, and professional experience.</p>

        <h4>🛠️ Features Included:</h4>
        <ul>
        <li><strong>Single Prediction:</strong> Predict salary for individual employees</li>
        <li><strong>Batch Prediction:</strong> Upload CSV files for multiple predictions</li>
        <li><strong>Data Visualization:</strong> Interactive charts and analysis</li>
        <li><strong>Export Results:</strong> Download predictions as CSV</li>
        <li><strong>Theme Customization:</strong> Light/Dark mode support</li>
        <li><strong>Responsive Design:</strong> Works on all devices</li>
        </ul>

        <h4>📊 Technology Stack:</h4>
        <ul>
        <li>Streamlit - Web application framework</li>
        <li>Scikit-learn - Machine learning model</li>
        <li>Plotly - Interactive visualizations</li>
        <li>Pandas - Data manipulation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
        st.markdown("""
        <div class="feature-card">
        <h4>👨‍💻 Developer</h4>
        <p>Built with ❤️ using Streamlit</p>
        <p><strong>Version:</strong> 2.0</p>
        <p><strong>Last Updated:</strong> 2024</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "💼 Salary Prediction System | Built with Streamlit | "
    "<a href='https://github.com/your-repo' target='_blank'>GitHub Repository</a>"
    "</div>",
    unsafe_allow_html=True
)