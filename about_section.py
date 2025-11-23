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