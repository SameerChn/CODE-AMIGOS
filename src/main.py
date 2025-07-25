import streamlit as st
import pandas as pd
import utils
import traceback
import os
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page config
st.set_page_config(page_title="CVision: Smart Job Finder", layout="wide")
# Add this CSS right after your st.set_page_config() call
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #FEFAE0;
        color: #000000;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #819067 !important;
    }
    
    /* Headers and titles */
    h1, h2, h3, h4, h5, h6 {
        color: #0A400C !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #0A400C;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }
    
    .stButton>button:hover {
        background-color: #819067;
        color: white;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #B1AB86;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Expanders */
    .stExpander {
        background-color: #FEFAE0;
        border: 1px solid #B1AB86;
        border-radius: 8px;
    }
    
    .stExpanderHeader {
        background-color: #B1AB86;
        color: #000000;
    }
    
    /* Dataframes/tables */
    .stDataFrame {
        border: 1px solid #B1AB86;
        border-radius: 8px;
    }
    
    /* Text input fields */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        color: #000000;
        background-color: #FEFAE0;
        border: 1px solid #B1AB86;
    }
    
    /* Checkboxes */
    .stCheckbox>label {
        color: #000000;
    }
    
    /* Info boxes */
    .stAlert-info {
        background-color: #B1AB86;
        color: #000000;
        border: 1px solid #0A400C;
    }
    
    /* Success boxes */
    .stAlert-success {
        background-color: #819067;
        color: white;
    }
    
    /* Warning boxes */
    .stAlert-warning {
        background-color: #B1AB86;
        color: #000000;
    }
    
    /* Error boxes */
    .stAlert-error {
        background-color: #B1AB86;
        color: #8B0000;
    }
    /* Black alert container */
    .stAlertContainer.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-ak.st-al.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-bc.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7 {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Horizontal lines */
    hr {
        border-color: #0A400C;
    }
    
    /* Link color */
    a {
        color: #0A400C !important;
    }
    
    /* Tabs */
    [data-baseweb="tab"] {
        background-color: #FEFAE0;
    }
    
    [data-baseweb="tab"]:hover {
        background-color: #B1AB86;
    }
    
    [aria-selected="true"] {
        background-color: #819067 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)
# App title and description
st.title("CVision: Smart Job Finder")
st.markdown("Upload your CV and find matching jobs based on your skills and experience.")

# Check for Tesseract OCR availability
if not utils.TESSERACT_AVAILABLE:
    st.warning("⚠️ Tesseract OCR is not installed or not found. OCR functionality for image-based PDFs will be limited.")
    if st.button("Install Tesseract OCR"):
        st.info("Starting Tesseract OCR installation... Please wait.")
        try:
            # Run the installer script
            install_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_tesseract.py")
            if os.path.exists(install_script_path):
                st.info("Please follow the installation wizard that will open. After installation is complete, restart this application.")
                os.system(f"{sys.executable} {install_script_path}")
            else:
                st.error(f"Installation script not found at {install_script_path}")
        except Exception as e:
            st.error(f"Error running Tesseract installer: {str(e)}")
            st.info("Please install Tesseract OCR manually from: https://github.com/UB-Mannheim/tesseract/wiki")
    st.markdown("---")

# Initialize session state variables if they don't exist
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = None
if 'domain' not in st.session_state:
    st.session_state.domain = None
if 'skills' not in st.session_state:
    st.session_state.skills = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'error_message' not in st.session_state:
    st.session_state.error_message = None
if 'gemini_analysis' not in st.session_state:
    st.session_state.gemini_analysis = None
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = None

# Set the API key in session state
st.session_state.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")

# Sidebar for CV upload and manual search
with st.sidebar:
    st.header("Upload Your CV")
    uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
    
    st.header("Or Search Manually")
    manual_domain = st.text_input("Enter a job domain (e.g., Software Engineering)")
    
    # Add manual text input for Gemini analysis
    st.header("Analyze Text with Gemini AI")
    manual_text_input = st.text_area("Enter text to analyze with Gemini AI", height=150, 
                                  help="Enter any text you want to analyze with Google's Gemini AI")
    analyze_text_button = st.button("Analyze Text with Gemini AI")
    
    # Handle manual text analysis
    if analyze_text_button and manual_text_input:
        with st.spinner("Analyzing text with Gemini AI..."):
            try:
                analysis_result = utils.analyze_manual_text_with_gemini(manual_text_input)
                if analysis_result:
                    st.subheader("Gemini AI Analysis Result")
                    st.markdown(analysis_result)
                else:
                    st.warning("Gemini analysis could not be generated")
            except Exception as e:
                st.error(f"Error analyzing text with Gemini AI: {str(e)}")
    elif analyze_text_button and not manual_text_input:
        st.warning("Please enter some text to analyze")

    st.header("Select Platforms")
    selected_platforms = st.multiselect(
        "Choose job platforms to search:",
        options=["LinkedIn", "Upwork", "Fiverr", "Indeed", "Naukri.com", "Internshala"],
        default=["LinkedIn", "Upwork", "Fiverr", "Indeed", "Naukri.com", "Internshala"]
    )
    
    # Google Gemini API configuration
    st.header("AI Analysis Settings")
    st.info("Google Gemini provides advanced resume and job analysis")
    
    # Check if Gemini API is available
    if utils.GEMINI_AVAILABLE:
        st.success("Gemini API is configured and ready to use")
    else:
        st.warning("⚠️ Gemini API is currently unavailable. This may be due to quota limits or service disruption.")
    
    use_gemini = st.checkbox("Enable Gemini AI Analysis", value=True)

    if st.button("Search Jobs by Domain"):
        if manual_domain:
            st.session_state.domain = manual_domain
            st.session_state.cv_text = None # Clear CV text for manual search
            st.session_state.skills = None
            st.session_state.jobs = []
            st.session_state.error_message = None
            print(f"\n===== MANUAL SEARCH FOR: {manual_domain} =====\n")
            try:
                all_jobs = []
                with st.spinner("Searching for jobs..."):
                    for platform in selected_platforms:
                        if platform == "LinkedIn":
                            linkedin_jobs = utils.scrape_linkedin(st.session_state.domain)
                            for job in linkedin_jobs:
                                job['platform'] = 'LinkedIn'
                            all_jobs.extend(linkedin_jobs)
                            print(f"Found {len(linkedin_jobs)} jobs on LinkedIn")
                        elif platform == "Upwork":
                            upwork_jobs = utils.scrape_upwork(st.session_state.domain)
                            for job in upwork_jobs:
                                job['platform'] = 'Upwork'
                            all_jobs.extend(upwork_jobs)
                            print(f"Found {len(upwork_jobs)} jobs on Upwork")
                        elif platform == "Fiverr":
                            fiverr_jobs = utils.scrape_fiverr(st.session_state.domain)
                            for job in fiverr_jobs:
                                job['platform'] = 'Fiverr'
                            all_jobs.extend(fiverr_jobs)
                            print(f"Found {len(fiverr_jobs)} jobs on Fiverr")
                        elif platform == "Indeed":
                            indeed_jobs = utils.scrape_indeed(st.session_state.domain)
                            for job in indeed_jobs:
                                job['platform'] = 'Indeed'
                            all_jobs.extend(indeed_jobs)
                            print(f"Found {len(indeed_jobs)} jobs on Indeed")
                        elif platform == "Naukri.com":
                            naukri_jobs = utils.scrape_naukri(st.session_state.domain)
                            for job in naukri_jobs:
                                job['platform'] = 'Naukri.com'
                            all_jobs.extend(naukri_jobs)
                            print(f"Found {len(naukri_jobs)} jobs on Naukri.com")
                        elif platform == "Internshala":
                            internshala_jobs = utils.scrape_internshala(st.session_state.domain)
                            for job in internshala_jobs:
                                job['platform'] = 'Internshala'
                            all_jobs.extend(internshala_jobs)
                            print(f"Found {len(internshala_jobs)} jobs on Internshala")
                st.session_state.jobs = all_jobs
            except Exception as e:
                print(f"Error finding jobs: {str(e)}")
                print(traceback.format_exc())
                st.error(f"Error finding jobs: {str(e)}")
        else:
            st.warning("Please enter a domain to search.")
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Extract text from CV
        try:
            print(f"\n\n===== PROCESSING NEW CV UPLOAD: {uploaded_file.name} =====\n")
            st.session_state.cv_text = utils.extract_text(uploaded_file)
            st.session_state.error_message = None
            
            # Check if the returned text is an error message
            if st.session_state.cv_text and isinstance(st.session_state.cv_text, str) and \
               (st.session_state.cv_text.startswith("Error") or \
                st.session_state.cv_text.startswith("This appears") or \
                st.session_state.cv_text.startswith("No text") or \
                st.session_state.cv_text.startswith("Unsupported")):
                
                st.session_state.error_message = st.session_state.cv_text
                st.session_state.cv_text = None
                st.error(st.session_state.error_message)
                print(f"Error message displayed to user: {st.session_state.error_message}")
            
            elif st.session_state.cv_text:
                print(f"Successfully extracted CV text: {len(st.session_state.cv_text)} characters")
                st.write(f"CV text extracted ({len(st.session_state.cv_text)} characters)")
                
                # Determine job domain
                try:
                    candidate_labels = [
                        # Technical Domains
                        "Software Engineering", "Data Science", "Machine Learning", "Artificial Intelligence", 
                        "Backend Development", "Frontend Development", "Full Stack Development", 
                        "DevOps Engineering", "Cloud Computing", "Mobile App Development",
                        "Game Development", "Cybersecurity", "Database Administration", "UI/UX Design",
                        "Blockchain Development", "IoT Development", "Embedded Systems", "QA Engineering",
                        
                        # Business Domains
                        "Marketing", "Digital Marketing", "Content Creation", "Sales", "Finance", 
                        "Accounting", "Human Resources", "Operations", "Project Management", 
                        "Product Management", "Business Analysis", "Customer Support",
                        "Supply Chain Management", "E-commerce", "Healthcare", "Education"
                    ]
                    
                    domain, confidence = utils.get_domain(st.session_state.cv_text, candidate_labels)
                    st.session_state.domain = domain
                    st.write(f"Detected domain: {domain} (Confidence: {confidence:.2f})")
                    print(f"Detected domain: {domain} (Confidence: {confidence:.2f})")
                except Exception as e:
                    print(f"Error determining job domain: {str(e)}")
                    print(traceback.format_exc())
                    st.error("Error determining job domain")
                
                # Extract skills
                try:
                    # Common skills across domains
                    skills_list = [
                        # Programming Languages
                        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust", 
                        "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Shell Scripting", "Bash",
                        "Assembly", "Objective-C", "Dart", "Groovy", "Lua", "Haskell", "Clojure",
                        
                        # Frontend Development
                        "HTML", "CSS", "React", "Angular", "Vue.js", "jQuery", "Bootstrap", "Tailwind CSS",
                        "Material UI", "Redux", "Next.js", "Gatsby", "Svelte", "Webpack", "Babel", "SASS",
                        "LESS", "Responsive Design", "Progressive Web Apps", "Web Components", "WebSockets",
                        
                        # Backend Development
                        "Node.js", "Express.js", "Django", "Flask", "Spring Boot", "Laravel", "Ruby on Rails",
                        "ASP.NET", "FastAPI", "GraphQL", "REST API", "Microservices", "Serverless",
                        "gRPC", "WebSockets", "Socket.io", "Nginx", "Apache", "OAuth", "JWT", "SOAP",
                        
                        # Database & Data Storage
                        "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server",
                        "Redis", "Elasticsearch", "Cassandra", "DynamoDB", "Firebase", "Neo4j", "Couchbase",
                        "MariaDB", "InfluxDB", "Supabase", "Fauna", "ORM", "Mongoose", "Sequelize", "Prisma",
                        
                        # DevOps & Cloud
                        "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "Bitbucket", "CI/CD",
                        "AWS", "Azure", "GCP", "Terraform", "Ansible", "Puppet", "Chef", "Prometheus",
                        "Grafana", "ELK Stack", "Heroku", "DigitalOcean", "Vercel", "Netlify", "CircleCI",
                        "Travis CI", "GitHub Actions", "Vagrant", "Helm", "Istio", "Service Mesh",
                        
                        # AI & Machine Learning
                        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow",
                        "PyTorch", "Keras", "Scikit-learn", "OpenCV", "NLTK", "spaCy", "Hugging Face",
                        "Transformers", "GPT", "BERT", "Neural Networks", "Reinforcement Learning",
                        "Supervised Learning", "Unsupervised Learning", "Transfer Learning", "LLMs",
                        "Generative AI", "MLOps", "Feature Engineering", "Model Deployment",
                        
                        # Data Science & Analytics
                        "Data Analysis", "Data Visualization", "Data Mining", "Big Data", "Hadoop",
                        "Spark", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Tableau",
                        "Power BI", "Looker", "Databricks", "ETL", "Data Warehousing", "Data Modeling",
                        "Statistical Analysis", "A/B Testing", "Regression Analysis", "Time Series Analysis",
                        
                        # Mobile Development
                        "Android", "iOS", "React Native", "Flutter", "Xamarin", "Ionic", "Swift UI",
                        "Jetpack Compose", "Mobile UI Design", "App Store Optimization", "Push Notifications",
                        "Mobile Analytics", "Responsive Design", "Cross-platform Development",
                        
                        # Game Development
                        "Unity", "Unreal Engine", "Godot", "Game Design", "3D Modeling", "Animation",
                        "Physics Engines", "Shader Programming", "Level Design", "Game AI", "Multiplayer",
                        
                        # Cybersecurity
                        "Network Security", "Penetration Testing", "Ethical Hacking", "Cryptography",
                        "Security Auditing", "Vulnerability Assessment", "OWASP", "Firewall Configuration",
                        "Intrusion Detection", "Security Compliance", "Identity Management", "Zero Trust",
                        
                        # Blockchain & Web3
                        "Blockchain", "Smart Contracts", "Solidity", "Ethereum", "Web3.js", "NFTs",
                        "DeFi", "Cryptocurrency", "Consensus Algorithms", "Distributed Ledger",
                        
                        # Project Management & Methodologies
                        "Agile", "Scrum", "Kanban", "Waterfall", "Lean", "Six Sigma", "JIRA",
                        "Confluence", "Trello", "Asana", "Monday.com", "MS Project", "Product Management",
                        "Sprint Planning", "Backlog Grooming", "User Stories", "Acceptance Criteria",
                        
                        # Design & Creative
                        "UI Design", "UX Design", "Figma", "Adobe XD", "Sketch", "Photoshop",
                        "Illustrator", "InDesign", "After Effects", "Premiere Pro", "Wireframing",
                        "Prototyping", "User Research", "Usability Testing", "Design Thinking",
                        
                        # Business & Marketing
                        "SEO", "SEM", "Content Marketing", "Social Media Marketing", "Email Marketing",
                        "Google Analytics", "CRM", "Salesforce", "HubSpot", "Market Research",
                        "Competitive Analysis", "Business Strategy", "Financial Analysis", "Budgeting",
                        
                        # Soft skills
                        "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
                        "Time Management", "Project Management", "Creativity", "Adaptability",
                        "Attention to Detail", "Emotional Intelligence", "Conflict Resolution",
                        "Negotiation", "Public Speaking", "Customer Service", "Mentoring", "Coaching",
                        "Decision Making", "Strategic Thinking", "Analytical Skills", "Interpersonal Skills"
                    ]
                    
                    st.session_state.skills = utils.extract_skills(st.session_state.cv_text, skills_list)
                    print(f"Extracted skills: {st.session_state.skills}")
                except Exception as e:
                    print(f"Error extracting skills: {str(e)}")
                    print(traceback.format_exc())
                    st.error("Error extracting skills")
                
                # Analyze resume with Gemini if enabled
                if use_gemini and st.session_state.gemini_api_key:
                    try:
                        with st.spinner("Analyzing resume with Google Gemini AI..."):
                            st.session_state.gemini_analysis = utils.analyze_resume_with_gemini(st.session_state.cv_text)
                            if st.session_state.gemini_analysis:
                                # Check if the analysis is an error message
                                if isinstance(st.session_state.gemini_analysis, str) and st.session_state.gemini_analysis.startswith("⚠️"):
                                    print("Gemini analysis returned an error message")
                                else:
                                    print("Gemini analysis completed successfully")
                            else:
                                print("Gemini analysis returned None")
                    except Exception as e:
                        print(f"Error in Gemini resume analysis: {str(e)}")
                        print(traceback.format_exc())
                        st.error("Error analyzing resume with Gemini AI")
            else:
                print("Failed to extract text from CV")
                st.error("Failed to extract text from CV. Please check the file format.")
        except Exception as e:
            print(f"Error processing CV: {str(e)}")
            print(traceback.format_exc())
            st.error(f"Error processing CV: {str(e)}")

# Main content area
if st.session_state.cv_text:
    # Display CV analysis
    st.header("CV Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Detected Domain")
        if st.session_state.domain:
            st.info(st.session_state.domain)
        else:
            st.warning("Domain could not be determined")
    
    with col2:
        st.subheader("Extracted Skills")
        if st.session_state.skills and len(st.session_state.skills) > 0:
            # Define skill categories for grouping
            skill_categories = {
                "Programming Languages": ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust", 
                                      "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Shell Scripting", "Bash",
                                      "Assembly", "Objective-C", "Dart", "Groovy", "Lua", "Haskell", "Clojure"],
                
                "Frontend": ["HTML", "CSS", "React", "Angular", "Vue.js", "jQuery", "Bootstrap", "Tailwind CSS",
                           "Material UI", "Redux", "Next.js", "Gatsby", "Svelte", "Webpack", "Babel", "SASS",
                           "LESS", "Responsive Design", "Progressive Web Apps", "Web Components", "WebSockets"],
                
                "Backend": ["Node.js", "Express.js", "Django", "Flask", "Spring Boot", "Laravel", "Ruby on Rails",
                          "ASP.NET", "FastAPI", "GraphQL", "REST API", "Microservices", "Serverless",
                          "gRPC", "WebSockets", "Socket.io", "Nginx", "Apache", "OAuth", "JWT", "SOAP"],
                
                "Database": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server",
                           "Redis", "Elasticsearch", "Cassandra", "DynamoDB", "Firebase", "Neo4j", "Couchbase",
                           "MariaDB", "InfluxDB", "Supabase", "Fauna", "ORM", "Mongoose", "Sequelize", "Prisma"],
                
                "DevOps & Cloud": ["Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "Bitbucket", "CI/CD",
                                 "AWS", "Azure", "GCP", "Terraform", "Ansible", "Puppet", "Chef", "Prometheus",
                                 "Grafana", "ELK Stack", "Heroku", "DigitalOcean", "Vercel", "Netlify", "CircleCI",
                                 "Travis CI", "GitHub Actions", "Vagrant", "Helm", "Istio", "Service Mesh"],
                
                "AI & ML": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow",
                          "PyTorch", "Keras", "Scikit-learn", "OpenCV", "NLTK", "spaCy", "Hugging Face",
                          "Transformers", "GPT", "BERT", "Neural Networks", "Reinforcement Learning",
                          "Supervised Learning", "Unsupervised Learning", "Transfer Learning", "LLMs",
                          "Generative AI", "MLOps", "Feature Engineering", "Model Deployment"],
                
                "Data Science": ["Data Analysis", "Data Visualization", "Data Mining", "Big Data", "Hadoop",
                               "Spark", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Tableau",
                               "Power BI", "Looker", "Databricks", "ETL", "Data Warehousing", "Data Modeling",
                               "Statistical Analysis", "A/B Testing", "Regression Analysis", "Time Series Analysis"],
                
                "Mobile": ["Android", "iOS", "React Native", "Flutter", "Xamarin", "Ionic", "Swift UI",
                         "Jetpack Compose", "Mobile UI Design", "App Store Optimization", "Push Notifications",
                         "Mobile Analytics", "Responsive Design", "Cross-platform Development"],
                
                "Other Technical": ["Game Development", "Unity", "Unreal Engine", "Godot", "3D Modeling", "Animation",
                                  "Cybersecurity", "Network Security", "Penetration Testing", "Ethical Hacking", "Cryptography",
                                  "Blockchain", "Smart Contracts", "Solidity", "Ethereum", "Web3.js", "NFTs"],
                
                "Soft Skills": ["Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
                              "Time Management", "Project Management", "Creativity", "Adaptability",
                              "Attention to Detail", "Emotional Intelligence", "Conflict Resolution",
                              "Negotiation", "Public Speaking", "Customer Service", "Mentoring", "Coaching",
                              "Decision Making", "Strategic Thinking", "Analytical Skills", "Interpersonal Skills"]
            }
            
            # Group extracted skills by category
            categorized_skills = {}
            for category, skills in skill_categories.items():
                matched_skills = [skill for skill in st.session_state.skills if skill in skills]
                if matched_skills:
                    categorized_skills[category] = matched_skills
            
            # Display skills by category
            if categorized_skills:
                for category, skills in categorized_skills.items():
                    with st.expander(f"{category} ({len(skills)})"):
                        st.write(", ".join(skills))
            
            # Display uncategorized skills
            all_categorized = [skill for category_skills in categorized_skills.values() for skill in category_skills]
            uncategorized = [skill for skill in st.session_state.skills if skill not in all_categorized]
            if uncategorized:
                with st.expander(f"Other Skills ({len(uncategorized)})"):
                    st.write(", ".join(uncategorized))
        else:
            st.warning("No skills were extracted")
    
    # Display Gemini AI Analysis if available
    if st.session_state.gemini_analysis:
        st.header("Gemini AI Resume Analysis")
        # Check if the analysis is an error message
        if isinstance(st.session_state.gemini_analysis, str) and st.session_state.gemini_analysis.startswith("⚠️"):
            st.warning(st.session_state.gemini_analysis)
        else:
            st.markdown(st.session_state.gemini_analysis)
    elif st.session_state.gemini_api_key and 'use_gemini' in locals() and use_gemini:
        if st.button("Analyze Resume with Gemini AI"):
            try:
                with st.spinner("Analyzing resume with Google Gemini AI..."):
                    st.session_state.gemini_analysis = utils.analyze_resume_with_gemini(st.session_state.cv_text)
                    if st.session_state.gemini_analysis:
                        st.markdown(st.session_state.gemini_analysis)
                    else:
                        st.warning("Gemini analysis could not be generated")
            except Exception as e:
                st.error(f"Error analyzing resume with Gemini AI: {str(e)}")
    else:
        st.info("Enable Gemini AI Analysis in the sidebar for advanced resume insights")
    
    # Job search section
    st.header("Find Matching Jobs")
    if st.button("Find Matching Jobs"):
        try:
            all_jobs = []
            print(f"\n===== SEARCHING JOBS FOR: {st.session_state.domain} =====\n")
            with st.spinner("Searching for jobs..."):
                for platform in selected_platforms:
                    if platform == "LinkedIn":
                        linkedin_jobs = utils.scrape_linkedin(st.session_state.domain)
                        for job in linkedin_jobs:
                            job['platform'] = 'LinkedIn'
                        all_jobs.extend(linkedin_jobs)
                        print(f"Found {len(linkedin_jobs)} jobs on LinkedIn")
                    elif platform == "Upwork":
                        upwork_jobs = utils.scrape_upwork(st.session_state.domain)
                        for job in upwork_jobs:
                            job['platform'] = 'Upwork'
                        all_jobs.extend(upwork_jobs)
                        print(f"Found {len(upwork_jobs)} jobs on Upwork")
                    elif platform == "Fiverr":
                        fiverr_jobs = utils.scrape_fiverr(st.session_state.domain)
                        for job in fiverr_jobs:
                            job['platform'] = 'Fiverr'
                        all_jobs.extend(fiverr_jobs)
                        print(f"Found {len(fiverr_jobs)} jobs on Fiverr")
                    elif platform == "Indeed":
                        indeed_jobs = utils.scrape_indeed(st.session_state.domain)
                        for job in indeed_jobs:
                            job['platform'] = 'Indeed'
                        all_jobs.extend(indeed_jobs)
                        print(f"Found {len(indeed_jobs)} jobs on Indeed")
                    elif platform == "Naukri.com":
                        naukri_jobs = utils.scrape_naukri(st.session_state.domain)
                        for job in naukri_jobs:
                            job['platform'] = 'Naukri.com'
                        all_jobs.extend(naukri_jobs)
                        print(f"Found {len(naukri_jobs)} jobs on Naukri.com")
                    elif platform == "Internshala":
                        internshala_jobs = utils.scrape_internshala(st.session_state.domain)
                        for job in internshala_jobs:
                            job['platform'] = 'Internshala'
                        all_jobs.extend(internshala_jobs)
                        print(f"Found {len(internshala_jobs)} jobs on Internshala")

            if all_jobs:
                print("Matching jobs to CV...")
                st.session_state.jobs = utils.match_jobs(st.session_state.cv_text, all_jobs)
                print(f"Matched {len(st.session_state.jobs)} jobs")
            else:
                print("No jobs found on selected platforms")
                st.warning("No jobs found on selected platforms")
        except Exception as e:
            print(f"Error finding jobs: {str(e)}")
            print(traceback.format_exc())
            st.error(f"Error finding jobs: {str(e)}")

elif st.session_state.domain and not st.session_state.cv_text:
    st.header(f"Job Search Results for: {st.session_state.domain}")

# Display matched jobs (for both CV-based and manual search)
if st.session_state.jobs and len(st.session_state.jobs) > 0:
    st.header("Matching Jobs")
    st.write(f"Found {len(st.session_state.jobs)} matching jobs")
    
    # Limit to 10 jobs
    jobs_to_display = st.session_state.jobs[:10]
    
    # Create a DataFrame for better display
    jobs_df = pd.DataFrame([
        {
            "Platform": job.get('platform', 'N/A'),
            "Title": job["title"],
            "Match Score": f"{job.get('match_score', 'N/A'):.2f}" if isinstance(job.get('match_score'), float) else 'N/A',
            "Link": job["link"]
        } for job in jobs_to_display
    ])
    
    # Display as a table with clickable links
    st.dataframe(
        jobs_df,
        column_config={
            "Link": st.column_config.LinkColumn("Job Link")
        },
        hide_index=True
    )
    
    # Display detailed job information with Gemini analysis
    st.header("Job Details and Analysis")
    for i, job in enumerate(jobs_to_display):
        with st.expander(f"{i+1}. {job['title']} ({job.get('platform', 'N/A')})"): 
            st.markdown(f"**Match Score:** {job.get('match_score', 'N/A'):.2f}" if isinstance(job.get('match_score'), float) else "**Match Score:** N/A")
            st.markdown(f"**Job Link:** [{job['link']}]({job['link']})")
            
            # Display Gemini analysis if available
            if 'gemini_analysis' in job and job['gemini_analysis']:
                st.subheader("Gemini AI Job Analysis")
                # Check if the analysis is an error message
                if isinstance(job['gemini_analysis'], str) and (job['gemini_analysis'].startswith("Error") or job['gemini_analysis'].startswith("⚠️")):
                    st.warning(job['gemini_analysis'])
                else:
                    st.markdown(job['gemini_analysis'])
            elif st.session_state.gemini_api_key and 'use_gemini' in locals() and use_gemini and st.session_state.cv_text:
                try:
                    with st.spinner("Analyzing job description with Google Gemini AI..."):
                        job_desc = utils.get_job_description(job['link'])
                        if job_desc:
                            analysis = utils.analyze_job_description_with_gemini(job_desc, st.session_state.cv_text)
                            if analysis:
                                job['gemini_analysis'] = analysis
                                # Check if the analysis is an error message
                                if isinstance(analysis, str) and (analysis.startswith("Error") or analysis.startswith("⚠️")):
                                    st.warning(analysis)
                                else:
                                    st.markdown(analysis)
                            else:
                                st.warning("Gemini analysis could not be generated")
                        else:
                            st.warning("Could not fetch job description")
                except Exception as e:
                    st.error(f"Error analyzing job with Gemini AI: {str(e)}")
            elif not ('use_gemini' in locals() and use_gemini):
                st.info("Enable Gemini AI Analysis in the sidebar for advanced job insights")

elif st.session_state.error_message:
    st.error(st.session_state.error_message)
    st.markdown("### Troubleshooting Tips")
    st.markdown("""
    - Make sure your PDF is text-based and not just scanned images
    - Try converting your CV to a DOCX format
    - Ensure your file is not corrupted or password-protected
    - Try a different CV file
    """)

# Show initial message only if no action has been taken
if not st.session_state.cv_text and not st.session_state.domain:
    st.info("Please upload your CV or enter a domain to get started")
    
    # Information about Gemini AI features
    st.header("New Feature: Google Gemini AI Integration")
    st.markdown("""
    ### Enhance Your Job Search with AI-Powered Analysis
    
    We've integrated Google's Gemini AI to provide advanced analysis of your resume and job descriptions:
    
    #### Resume Analysis Features:
    - Identify key skills and expertise in your resume
    - Highlight strengths of your resume
    - Suggest improvements to make your resume more effective
    - Recommend job roles that would be a good fit for your profile
    - Provide a comprehensive summary of your professional profile
    
    #### Job Description Analysis Features:
    - Identify key requirements and skills needed for each job
    - Evaluate how well your profile matches the job requirements
    - Highlight your strengths relevant to specific positions
    - Identify gaps in your profile compared to job requirements
    - Provide specific suggestions to improve your application
    - Rate your overall match on a scale of 1-10 with detailed explanation
    
    To use these features:
    1. Enable Gemini AI Analysis in the sidebar (already configured with API key)
    2. Upload your resume or search for jobs
    3. View the AI-powered analysis of your resume and job matches
    
    Start experiencing the power of AI in your job search today!
    """)
    
    # Display a visual separator
    st.markdown("---")