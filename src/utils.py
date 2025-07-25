# Helper functions for NLP, scraping, and matching will go here.
import io
import pdfplumber
import docx
import spacy
import pytesseract
from PIL import Image
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import traceback
import re
import os
import sys

# Configure Tesseract OCR path
TESSERACT_AVAILABLE = True
try:
    # Check if tesseract is available
    from shutil import which
    tesseract_path = which('tesseract')
    
    if not tesseract_path:
        # On Windows, try common installation paths
        if sys.platform.startswith('win'):
            common_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract-OCR\tesseract.exe'
            ]
            for path in common_paths:
                if os.path.exists(path):
                    tesseract_path = path
                    break
    
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        print(f"Tesseract OCR configured at: {tesseract_path}")
    else:
        print("Tesseract OCR not found. OCR functionality will be limited.")
        print("Please install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
        TESSERACT_AVAILABLE = False
except Exception as e:
    print(f"Error configuring Tesseract OCR: {str(e)}")
    TESSERACT_AVAILABLE = False

# Import Google Gemini API
try:
    print("Loading Google Gemini API...")
    import google.generativeai as genai
    # Configure Gemini API with the provided key
    genai.configure(api_key="AIzaSyAa97pSL3kb1yEvoaj6vpi8LCeN6aRvMPk")
    print("Google Gemini API loaded successfully")
    
    # Check if the API is actually working by listing models
    try:
        models = list(genai.list_models())
        if models:
            print(f"Successfully listed {len(models)} Gemini models")
            GEMINI_AVAILABLE = True
        else:
            print("No Gemini models available")
            GEMINI_AVAILABLE = False
    except Exception as model_error:
        print(f"Error listing Gemini models: {str(model_error)}")
        print(traceback.format_exc())
        GEMINI_AVAILABLE = False
except Exception as e:
    print(f"Error loading Google Gemini API: {str(e)}")
    print(traceback.format_exc())
    GEMINI_AVAILABLE = False

# Load Sentence Transformer model
try:
    print("Loading SentenceTransformer model...")
    similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("SentenceTransformer model loaded successfully")
except Exception as e:
    print(f"Error loading SentenceTransformer model: {str(e)}")
    print(traceback.format_exc())
    similarity_model = None

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Load spaCy model
try:
    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_sm")
    print("spaCy model loaded successfully")
except Exception as e:
    print(f"Error loading spaCy model: {str(e)}")
    print(traceback.format_exc())
    nlp = None

# Zero-shot classification pipeline
try:
    print("Loading zero-shot classification pipeline...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("Zero-shot classification pipeline loaded successfully")
except Exception as e:
    print(f"Error loading zero-shot classification pipeline: {str(e)}")
    print(traceback.format_exc())
    classifier = None


def extract_text(uploaded_file):
    print(f"Extracting text from {uploaded_file.name}, type: {type(uploaded_file)}")
    try:
        # Debug file content
        file_bytes = uploaded_file.getvalue()
        print(f"File size: {len(file_bytes)} bytes")
        
        if uploaded_file.name.endswith('.pdf'):
            print("Processing PDF file...")
            with io.BytesIO(file_bytes) as f:
                try:
                    with pdfplumber.open(f) as pdf:
                        print(f"PDF has {len(pdf.pages)} pages")
                        text = ""
                        for i, page in enumerate(pdf.pages):
                            try:
                                page_text = page.extract_text()
                                print(f"Page {i+1}: Extracted {len(page_text) if page_text else 0} characters")
                                text += page_text if page_text else ""
                            except Exception as e:
                                print(f"Error extracting text from page {i+1}: {str(e)}")
                        
                        # Check if we got any text
                        if not text or len(text.strip()) == 0:
                            print("No text extracted from PDF. Attempting OCR...")
                            
                            # Check if Tesseract is available
                            if not TESSERACT_AVAILABLE:
                                print("Tesseract OCR is not available.")
                                return "This appears to be an image-based PDF, but OCR is not available. Please install Tesseract OCR or upload a text-based PDF or DOCX file."
                            
                            try:
                                f.seek(0) # Reset file pointer
                                ocr_text = ""
                                with pdfplumber.open(f) as pdf:
                                    for i, page in enumerate(pdf.pages):
                                        try:
                                            im = page.to_image(resolution=300).original
                                            page_ocr_text = pytesseract.image_to_string(im, lang='eng')
                                            print(f"Page {i+1} OCR: Extracted {len(page_ocr_text)} characters")
                                            ocr_text += page_ocr_text if page_ocr_text else ""
                                        except Exception as ocr_error:
                                            print(f"Error during OCR on page {i+1}: {str(ocr_error)}")
                                if not ocr_text or len(ocr_text.strip()) == 0:
                                    print("OCR did not yield any text.")
                                    return "This appears to be an image-based PDF, but OCR failed. Please upload a text-based PDF or DOCX file."
                                print(f"Extracted total of {len(ocr_text)} characters from PDF using OCR")
                                return ocr_text
                            except Exception as e:
                                print(f"Error during OCR processing: {str(e)}")
                                print(traceback.format_exc())
                                return "Error processing image-based PDF with OCR. Please try a different file."
                        
                        print(f"Extracted total of {len(text)} characters from PDF")
                        return text
                except Exception as e:
                    print(f"Error opening PDF with pdfplumber: {str(e)}")
                    print(traceback.format_exc())
                    return "Error processing PDF file. Please try a different file."
            
        elif uploaded_file.name.endswith('.docx'):
            print("Processing DOCX file...")
            with io.BytesIO(file_bytes) as f:
                try:
                    doc = docx.Document(f)
                    paragraphs = [para.text for para in doc.paragraphs]
                    print(f"DOCX has {len(paragraphs)} paragraphs")
                    text = "\n".join(paragraphs)
                    
                    # Check if we got any text
                    if not text or len(text.strip()) == 0:
                        print("No text extracted from DOCX.")
                        return "No text could be extracted from this DOCX file. Please check the file content."
                    
                    print(f"Extracted {len(text)} characters from DOCX")
                    return text
                except Exception as e:
                    print(f"Error processing DOCX with python-docx: {str(e)}")
                    print(traceback.format_exc())
                    return "Error processing DOCX file. Please try a different file."
        
        print(f"Unsupported file format: {uploaded_file.name}")
        return "Unsupported file format. Please upload a PDF or DOCX file."
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        print(traceback.format_exc())
        return "Error processing file. Please try again with a different file."

def get_domain(text, candidate_labels):
    if not classifier:
        print("Zero-shot classifier not available")
        return "Unknown", 0.0
    
    # Check if text is an error message
    if text and isinstance(text, str) and text.startswith("Error") or text.startswith("This appears to be"):
        print(f"Text appears to be an error message: {text}")
        return "Unknown", 0.0
    
    try:
        print(f"Classifying text ({len(text)} chars) with {len(candidate_labels)} candidate labels")
        result = classifier(text, candidate_labels)
        print(f"Classification result: {result['labels'][0]} with score {result['scores'][0]:.2f}")
        return result['labels'][0], result['scores'][0]
    except Exception as e:
        print(f"Error in domain classification: {str(e)}")
        print(traceback.format_exc())
        return "Unknown", 0.0

def extract_skills(text, skills_list):
    if not nlp:
        print("spaCy model not available")
        return []
    
    # Check if text is an error message
    if text and isinstance(text, str) and text.startswith("Error") or text.startswith("This appears to be"):
        print(f"Text appears to be an error message: {text}")
        return []
    
    try:
        print(f"Extracting skills from text ({len(text)} chars) with {len(skills_list)} skills")
        doc = nlp(text.lower())
        found_skills = set()
        for skill in skills_list:
            if skill.lower() in doc.text:
                found_skills.add(skill)
                print(f"Found skill: {skill}")
        print(f"Extracted {len(found_skills)} skills")
        return list(found_skills)
    except Exception as e:
        print(f"Error extracting skills: {str(e)}")
        print(traceback.format_exc())
        return []

def scrape_linkedin(domain, location="India"):
    print(f"Scraping LinkedIn jobs for domain: {domain}, location: {location}")
    jobs = []
    url = f"https://www.linkedin.com/jobs/search/?keywords={domain.replace(' ', '%20')}&location={location}"
    try:
        print(f"Requesting URL: {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}, timeout=20)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"LinkedIn Page Title: {soup.title.string if soup.title else 'No Title'}")
        job_postings = soup.find_all("div", class_="base-card")
        print(f"Found {len(job_postings)} job postings")

        for job in job_postings:
            title_element = job.find("h3", class_="base-search-card__title")
            link_element = job.find("a", class_="base-card__full-link")
            if title_element and link_element:
                jobs.append({
                    'title': title_element.text.strip(),
                    'link': link_element['href'],
                    'source': 'LinkedIn'
                })
                print(f"Added job: {title_element.text.strip()}")
        print(f"Scraped {len(jobs)} jobs from LinkedIn")
    except Exception as e:
        print(f"Error scraping LinkedIn: {e}")
        print(traceback.format_exc())
    return jobs

def scrape_upwork(domain):
    print(f"Scraping Upwork jobs for domain: {domain}")
    jobs = []
    url = f"https://www.upwork.com/nx/jobs/search/?q={domain.replace(' ', '%20')}"
    try:
        print(f"Requesting URL: {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}, timeout=20)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        job_postings = soup.find_all("section", class_="air-card-hover") # Note: Upwork selectors change frequently
        print(f"Found {len(job_postings)} job postings on Upwork")

        for job in job_postings:
            title_element = job.find("h4")
            link_element = job.find("a", class_="job-title-link")
            if title_element and link_element:
                jobs.append({
                    'title': title_element.text.strip(),
                    'link': f"https://www.upwork.com{link_element['href']}",
                    'source': 'Upwork'
                })
                print(f"Added job: {title_element.text.strip()}")
        print(f"Scraped {len(jobs)} jobs from Upwork")
    except Exception as e:
        print(f"Error scraping Upwork: {e}")
        print(traceback.format_exc())
    return jobs

def scrape_fiverr(domain):
    print(f"Scraping Fiverr jobs for domain: {domain}")
    jobs = []
    url = f"https://www.fiverr.com/search/gigs?query={domain.replace(' ', '%20')}"
    try:
        print(f"Requesting URL: {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}, timeout=20)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Fiverr Page Title: {soup.title.string if soup.title else 'No Title'}")
        job_postings = soup.select("div.gig-card-layout") # Using select for CSS selector
        print(f"Found {len(job_postings)} job postings on Fiverr")

        for job in job_postings:
            title_element = job.select_one("h3") # Using select_one
            link_element = job.select_one("a")
            if title_element and link_element:
                jobs.append({
                    'title': title_element.text.strip(),
                    'link': f"https://www.fiverr.com{link_element['href']}",
                    'source': 'Fiverr'
                })
                print(f"Added job: {title_element.text.strip()}")
        print(f"Scraped {len(jobs)} jobs from Fiverr")
    except Exception as e:
        print(f"Error scraping Fiverr: {e}")
        print(traceback.format_exc())
    return jobs

def scrape_indeed(domain, location="India"):
    print(f"Scraping Indeed jobs for domain: {domain}, location: {location}")
    jobs = []
    url = f"https://www.indeed.com/jobs?q={domain.replace(' ', '+')}&l={location.replace(' ', '+')}"
    try:
        print(f"Requesting URL: {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}, timeout=20)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Indeed Page Title: {soup.title.string if soup.title else 'No Title'}")
        job_postings = soup.select("div.jobsearch-SerpJobCard")
        print(f"Found {len(job_postings)} job postings on Indeed")

        for job in job_postings:
            title_element = job.select_one("h2.title a")
            if title_element:
                jobs.append({
                    'title': title_element.text.strip(),
                    'link': f"https://www.indeed.com{title_element['href']}",
                    'source': 'Indeed'
                })
                print(f"Added job: {title_element.text.strip()}")
        print(f"Scraped {len(jobs)} jobs from Indeed")
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
        print(traceback.format_exc())
    return jobs

def scrape_naukri(domain, location="India"):
    print(f"Scraping Naukri jobs for domain: {domain}, location: {location}")
    jobs = []
    url = f"https://www.naukri.com/{domain.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"
    try:
        print(f"Requesting URL: {url} with Selenium")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--log-level=3')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(5)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        print(f"Naukri Page Title: {soup.title.string if soup.title else 'No Title'}")
        job_postings = soup.select("article.jobTuple")
        print(f"Found {len(job_postings)} job postings on Naukri.com")

        for job in job_postings:
            title_element = job.select_one("a.title")
            if title_element:
                jobs.append({
                    'title': title_element.text.strip(),
                    'link': title_element['href'],
                    'source': 'Naukri.com'
                })
                print(f"Added job: {title_element.text.strip()}")
        print(f"Scraped {len(jobs)} jobs from Naukri.com")
    except Exception as e:
        print(f"Error scraping Naukri.com: {e}")
        print(traceback.format_exc())
    return jobs

def scrape_internshala(domain):
    print(f"Scraping Internshala jobs for domain: {domain}")
    jobs = []
    url = f"https://internshala.com/internships/keywords-{domain.replace(' ', '%20')}"
    try:
        print(f"Requesting URL: {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}, timeout=20)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Internshala Page Title: {soup.title.string if soup.title else 'No Title'}")
        job_postings = soup.select("div.individual_internship") # Corrected selector
        print(f"Found {len(job_postings)} job postings on Internshala")

        for job in job_postings:
            title_element = job.select_one("h3.heading_4_5")
            link_element = job.select_one("a.view_detail_button")
            if title_element and link_element:
                jobs.append({
                    'title': title_element.text.strip(),
                    'link': f"https://internshala.com{link_element['href']}",
                    'source': 'Internshala'
                })
                print(f"Added job: {title_element.text.strip()}")
        print(f"Scraped {len(jobs)} jobs from Internshala")
    except Exception as e:
        print(f"Error scraping Internshala: {e}")
        print(traceback.format_exc())
    return jobs

def get_job_description(job_url):
    try:
        print(f"Fetching job description from: {job_url}")
        response = requests.get(job_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # This class might change, need to inspect the job page HTML
        desc_container = soup.find("div", class_="show-more-less-html__markup")
        if desc_container:
            desc_text = desc_container.text.strip()
            print(f"Extracted job description: {len(desc_text)} characters")
            return desc_text
        else:
            print("No job description found")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job description from {job_url}: {e}")
        print(traceback.format_exc())
        return ""

def analyze_resume_with_gemini(cv_text):
    """Analyze a resume using Google Gemini AI and provide insights."""
    if not GEMINI_AVAILABLE:
        print("Google Gemini API not available")
        return "⚠️ **Gemini AI Analysis Unavailable**\n\nThe Google Gemini API service is currently unavailable. This could be due to:\n\n- API quota limits exceeded\n- Service disruption\n- API key configuration issues\n\nPlease try again later or contact support if the issue persists."
    
    # Check if cv_text is an error message
    if cv_text and isinstance(cv_text, str) and (cv_text.startswith("Error") or cv_text.startswith("This appears to be")):
        print(f"CV text appears to be an error message: {cv_text}")
        return None
    
    try:
        print(f"Analyzing resume with Gemini ({len(cv_text)} chars)")
        
        # Try to use available models in order of preference
        available_models = []
        try:
            for model in genai.list_models():
                available_models.append(model.name)
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return "⚠️ **Gemini AI Analysis Unavailable**\n\nUnable to access Gemini AI models. This could be due to API quota limits or service disruption. Please try again later."
        
        # Try to find a suitable model
        model_name = None
        preferred_models = [
            'models/gemini-1.5-flash-latest',  # Prioritize Gemini 1.5 Flash Latest as requested
            'models/gemini-1.5-flash',        # Fallback to regular Gemini 1.5 Flash
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro',
            'models/gemini-1.0-pro-latest',
            'models/gemini-2.0-flash',
            'models/gemini-2.0-flash-001',
            'models/gemini-2.0-flash-lite',
            'models/gemini-2.0-flash-lite-001'
        ]
        
        # First try preferred models
        for preferred in preferred_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        # If no preferred models found, try any model with 'flash' in the name
        if not model_name:
            for name in available_models:
                if 'flash' in name.lower() and 'preview' not in name.lower():
                    model_name = name
                    break
        
        if not model_name:
            print("No suitable Gemini model found")
            return "⚠️ **Gemini AI Analysis Unavailable**\n\nNo suitable Gemini AI models are available. This could be due to API quota limits or service disruption. Please try again later."
        
        print(f"Using Gemini model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # Create the prompt for resume analysis
        prompt = f"""
        You are a professional resume analyzer using the advanced Gemini 1.5 Flash model. Please analyze the following resume and provide detailed insights:
        
        1. Key Skills and Expertise:
           - Identify both technical and soft skills present in the resume
           - Categorize skills by proficiency level (if possible)
           - Note any specialized or in-demand skills
        
        2. Resume Strengths:
           - Highlight the most impressive achievements and qualifications
           - Identify effective presentation elements
           - Note any unique selling points that make this candidate stand out
        
        3. Suggested Improvements:
           - Identify specific areas where the resume could be strengthened
           - Suggest additional information that could enhance the resume
           - Recommend formatting or structural changes if needed
           - Provide examples of how to better quantify achievements
        
        4. Recommended Job Roles:
           - List 3-5 specific job titles that would be a good match
           - For each role, explain why it's a good fit based on the resume
           - Suggest any emerging roles that might align with their skills
        
        5. Career Development Recommendations:
           - Suggest skills or certifications to acquire for career advancement
           - Identify potential career progression paths
        
        6. Candidate Profile Summary:
           - Provide a concise professional summary
           - Highlight the candidate's unique value proposition
        
        Resume text:
        {cv_text}
        
        Provide your analysis in a structured format with clear headings for each section. Be specific, actionable, and insightful in your analysis.
        """
        
        # Generate the analysis
        response = model.generate_content(prompt)
        analysis = response.text
        print(f"Generated resume analysis: {len(analysis)} characters")
        return analysis
    except Exception as e:
        print(f"Error analyzing resume with Gemini: {str(e)}")
        print(traceback.format_exc())
        
        # Check for quota exceeded errors
        error_str = str(e).lower()
        if "quota" in error_str or "rate limit" in error_str or "429" in error_str:
            return "⚠️ **Gemini AI Quota Exceeded**\n\nThe Google Gemini API quota has been exceeded. Please try again later or contact support for assistance."
        
        return "⚠️ **Gemini AI Analysis Error**\n\nAn error occurred while analyzing your resume with Gemini AI. Please try again later or contact support if the issue persists."

def analyze_manual_text_with_gemini(text_input):
    """Analyze manually entered text using Google Gemini AI and provide insights."""
    if not GEMINI_AVAILABLE:
        print("Google Gemini API not available")
        return "⚠️ **Gemini AI Analysis Unavailable**\n\nThe Google Gemini API service is currently unavailable. This could be due to:\n\n- API quota limits exceeded\n- Service disruption\n- API key configuration issues\n\nPlease try again later or contact support if the issue persists."
    
    try:
        print(f"Analyzing manual text input with Gemini ({len(text_input)} chars)")
        
        # Try to use available models in order of preference
        available_models = []
        try:
            for model in genai.list_models():
                available_models.append(model.name)
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return "⚠️ **Gemini AI Analysis Unavailable**\n\nUnable to access Gemini AI models. This could be due to API quota limits or service disruption. Please try again later."
        
        # Try to find a suitable model
        model_name = None
        preferred_models = [
            'models/gemini-1.5-flash-latest',  # Prioritize Gemini 1.5 Flash Latest as requested
            'models/gemini-1.5-flash',        # Fallback to regular Gemini 1.5 Flash
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro',
            'models/gemini-1.0-pro-latest',
            'models/gemini-2.0-flash',
            'models/gemini-2.0-flash-001',
            'models/gemini-2.0-flash-lite',
            'models/gemini-2.0-flash-lite-001'
        ]
        
        # First try preferred models
        for preferred in preferred_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        # If no preferred models found, try any model with 'flash' in the name
        if not model_name:
            for name in available_models:
                if 'flash' in name.lower() and 'preview' not in name.lower():
                    model_name = name
                    break
        
        if not model_name:
            print("No suitable Gemini model found")
            return "⚠️ **Gemini AI Analysis Unavailable**\n\nNo suitable Gemini AI models are available. This could be due to API quota limits or service disruption. Please try again later."
        
        print(f"Using Gemini model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # Create the prompt for text analysis
        prompt = f"""
        You are a professional AI assistant using the advanced Gemini 1.5 Flash model. Please analyze the following text and provide comprehensive insights:
        
        1. Executive Summary:
           - Provide a concise overview of the main points (3-5 sentences)
           - Identify the primary purpose or intent of the text
        
        2. Key Concepts and Entities:
           - List and explain important concepts, terms, and entities mentioned
           - Categorize them by relevance and domain
           - Highlight any specialized terminology with definitions
        
        3. Detailed Analysis:
           - Break down the main arguments or points presented
           - Identify any logical structure or progression of ideas
           - Note any evidence, examples, or data provided to support claims
           - Detect any biases, assumptions, or limitations in the text
        
        4. Contextual Information:
           - Provide relevant background or historical context
           - Connect the content to broader fields or disciplines
           - Explain any references that might not be immediately clear
        
        5. Questions and Answers:
           - Identify and answer any explicit questions in the text
           - Address implied questions or information gaps
        
        6. Related Topics and Further Exploration:
           - Suggest 3-5 related topics that could expand understanding
           - Recommend specific resources or approaches for deeper investigation
           - Identify potential applications or implications of the information
        
        7. Visual Representation (if applicable):
           - Suggest how this information could be visualized (charts, diagrams, etc.)
        
        Text to analyze:
        {text_input}
        
        Provide your analysis in a structured format with clear headings for each section. Be specific, insightful, and thorough in your analysis while maintaining clarity and readability.
        """
        
        # Generate the analysis
        response = model.generate_content(prompt)
        analysis = response.text
        print(f"Generated text analysis: {len(analysis)} characters")
        return analysis
    except Exception as e:
        print(f"Error analyzing text with Gemini: {str(e)}")
        print(traceback.format_exc())
        
        # Check for quota exceeded errors
        error_str = str(e).lower()
        if "quota" in error_str or "rate limit" in error_str or "429" in error_str:
            return "⚠️ **Gemini AI Quota Exceeded**\n\nThe Google Gemini API quota has been exceeded. Please try again later or contact support for assistance."
        
        return "⚠️ **Gemini AI Analysis Error**\n\nAn error occurred while analyzing your text with Gemini AI. Please try again later or contact support if the issue persists."

def analyze_job_description_with_gemini(job_desc, cv_text=None):
    """Analyze a job description using Google Gemini AI and provide insights."""
    if not GEMINI_AVAILABLE:
        print("Google Gemini API not available")
        return "⚠️ **Gemini AI Analysis Unavailable**\n\nThe Google Gemini API service is currently unavailable. This could be due to:\n\n- API quota limits exceeded\n- Service disruption\n- API key configuration issues\n\nPlease try again later or contact support if the issue persists."
    
    try:
        print(f"Analyzing job description with Gemini ({len(job_desc)} chars)")
        
        # Try to use available models in order of preference
        available_models = []
        try:
            for model in genai.list_models():
                available_models.append(model.name)
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return "⚠️ **Gemini AI Analysis Unavailable**\n\nUnable to access Gemini AI models. This could be due to API quota limits or service disruption. Please try again later."
        
        # Try to find a suitable model
        model_name = None
        preferred_models = [
            'models/gemini-1.5-flash-latest',  # Prioritize Gemini 1.5 Flash Latest as requested
            'models/gemini-1.5-flash',        # Fallback to regular Gemini 1.5 Flash
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro',
            'models/gemini-1.0-pro-latest',
            'models/gemini-2.0-flash',
            'models/gemini-2.0-flash-001',
            'models/gemini-2.0-flash-lite',
            'models/gemini-2.0-flash-lite-001'
        ]
        
        # First try preferred models
        for preferred in preferred_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        # If no preferred models found, try any model with 'flash' in the name
        if not model_name:
            for name in available_models:
                if 'flash' in name.lower() and 'preview' not in name.lower():
                    model_name = name
                    break
        
        if not model_name:
            print("No suitable Gemini model found")
            return "⚠️ **Gemini AI Analysis Unavailable**\n\nNo suitable Gemini AI models are available. This could be due to API quota limits or service disruption. Please try again later."
        
        print(f"Using Gemini model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # Create the prompt for job description analysis
        if cv_text:
            prompt = f"""
            You are a professional job application advisor using the advanced Gemini 1.5 Flash model. Please analyze the following job description 
            and the candidate's resume to provide comprehensive insights:
            
            1. Job Requirements Analysis:
               - List all explicit requirements (technical skills, experience, education, etc.)
               - Identify implicit requirements (soft skills, cultural fit indicators)
               - Categorize requirements as "must-have" vs "nice-to-have"
               - Note any unusual or specialized requirements
            
            2. Candidate Match Evaluation:
               - Provide a detailed assessment of how the candidate's profile aligns with each key requirement
               - Use specific examples from the resume to support your evaluation
               - Quantify the match for major requirement categories (e.g., technical skills: 80% match)
            
            3. Candidate Strengths for This Position:
               - Highlight 3-5 specific strengths that make the candidate competitive
               - Explain how each strength directly relates to job requirements or would add value
               - Suggest how to emphasize these strengths in a cover letter or interview
            
            4. Candidate Gaps Analysis:
               - Identify specific requirements where the candidate lacks experience or qualifications
               - Assess the significance of each gap (critical, moderate, minor)
               - Suggest how the candidate might address or compensate for each gap
            
            5. Application Enhancement Strategy:
               - Provide specific resume tailoring recommendations for this job
               - Suggest talking points for cover letter and interview responses
               - Recommend how to frame existing experience to better align with job requirements
               - Suggest any quick-win skills or certifications that could improve the application
            
            6. Competitive Analysis:
               - Identify likely strengths and weaknesses compared to typical applicants
               - Suggest unique selling points to differentiate the candidate
            
            7. Overall Match Rating:
               - Rate the overall match on a scale of 1-10 with decimal precision
               - Break down the rating by major requirement categories
               - Explain your rating with specific justifications
               - Provide an honest assessment of application success probability
            
            Job Description:
            {job_desc}
            
            Candidate's Resume:
            {cv_text}
            
            Provide your analysis in a structured format with clear headings for each section. Be specific, actionable, and honest in your assessment.
            """
        else:
            prompt = f"""
            You are a professional job analyst using the advanced Gemini 1.5 Flash model. Please analyze the following job description and provide comprehensive insights:
            
            1. Job Overview:
               - Summarize the position in 2-3 sentences
               - Identify the industry, company type, and role level
               - Note any unique aspects of this position
            
            2. Key Requirements Analysis:
               - List and categorize all technical skills required
               - Identify experience requirements (years, specific domains, etc.)
               - Note education, certification, or credential requirements
               - Highlight soft skills and personal attributes mentioned
               - Identify any unusual or specialized requirements
            
            3. Responsibilities Breakdown:
               - List and categorize all major responsibilities
               - Identify primary vs. secondary duties
               - Note any leadership, management, or cross-functional responsibilities
               - Identify potential challenges or high-pressure aspects of the role
            
            4. Compensation and Benefits Assessment (if mentioned):
               - Analyze the compensation relative to industry standards
               - Highlight any unique or valuable benefits
            
            5. Company Culture Indicators:
               - Identify language that reveals company values or culture
               - Note any mentions of work environment or team dynamics
            
            6. Ideal Candidate Profile:
               - Create a detailed profile of the ideal candidate
               - Identify the most critical qualifications vs. preferred qualifications
               - Suggest career background that would be most competitive
            
            7. Application Strategy Recommendations:
               - Suggest how candidates should tailor their applications
               - Identify key points to emphasize in cover letters and interviews
               - Note any potential red flags or areas requiring clarification
            
            8. Market Context:
               - Indicate how common or rare this type of position is
               - Suggest the likely competitiveness of the application process
               - Identify related roles that might require similar qualifications
            
            Job Description:
            {job_desc}
            
            Provide your analysis in a structured format with clear headings for each section. Be specific, insightful, and thorough in your analysis.
            """
        
        # Generate the analysis
        response = model.generate_content(prompt)
        analysis = response.text
        print(f"Generated job description analysis: {len(analysis)} characters")
        return analysis
    except Exception as e:
        print(f"Error analyzing job description with Gemini: {str(e)}")
        print(traceback.format_exc())
        
        # Check for quota exceeded errors
        error_str = str(e).lower()
        if "quota" in error_str or "rate limit" in error_str or "429" in error_str:
            return "⚠️ **Gemini AI Quota Exceeded**\n\nThe Google Gemini API quota has been exceeded. Please try again later or contact support for assistance."
        
        return "⚠️ **Gemini AI Analysis Error**\n\nAn error occurred while analyzing the job description with Gemini AI. Please try again later or contact support if the issue persists."

def match_jobs(cv_text, jobs):
    if not similarity_model:
        print("SentenceTransformer model not available")
        return []
    
    # Check if cv_text is an error message
    if cv_text and isinstance(cv_text, str) and cv_text.startswith("Error") or cv_text.startswith("This appears to be"):
        print(f"CV text appears to be an error message: {cv_text}")
        return []
    
    print(f"Matching CV text ({len(cv_text)} chars) with {len(jobs)} jobs")
    try:
        print("Encoding CV text...")
        cv_embedding = similarity_model.encode(cv_text, convert_to_tensor=True)
        print("CV text encoded successfully")
        matched_jobs = []

        # Import Google Generative AI
        from google import genai
        
        # Configure the API with the key
        genai.configure(api_key='AIzaSyAa97pSL3kb1yEvoaj6vpi8LCeN6aRvMPk')
        
        for job in jobs:
            try:
                job_desc = get_job_description(job['link'])
                if job_desc:
                    print(f"Encoding job description for {job['title']}...")
                    job_embedding = similarity_model.encode(job_desc, convert_to_tensor=True)
                    score = util.pytorch_cos_sim(cv_embedding, job_embedding).item()
                    job['match_score'] = score
                    
                    # Add Gemini analysis if available
                    try:
                        if GEMINI_AVAILABLE:
                            # Try to use available models in order of preference
                            available_models = []
                            try:
                                for model in genai.list_models():
                                    available_models.append(model.name)
                            except Exception as e:
                                print(f"Error listing models: {str(e)}")
                                job['gemini_analysis'] = "⚠️ **Gemini AI Analysis Unavailable**\n\nUnable to access Gemini AI models. This could be due to API quota limits or service disruption. Please try again later."
                                matched_jobs.append(job)
                                continue
                            
                            # Try to find a suitable model
                            model_name = None
                            preferred_models = [
                                'models/gemini-1.5-flash-latest',  # Prioritize Gemini 1.5 Flash Latest as requested
                                'models/gemini-1.5-flash',        # Fallback to regular Gemini 1.5 Flash
                                'models/gemini-1.5-pro',
                                'models/gemini-1.0-pro',
                                'models/gemini-1.0-pro-latest',
                                'models/gemini-2.0-flash',
                                'models/gemini-2.0-flash-001',
                                'models/gemini-2.0-flash-lite',
                                'models/gemini-2.0-flash-lite-001'
                            ]
                            
                            # First try preferred models
                            for preferred in preferred_models:
                                if preferred in available_models:
                                    model_name = preferred
                                    break
                            
                            # If no preferred models found, try any model with 'flash' in the name
                            if not model_name:
                                for name in available_models:
                                    if 'flash' in name.lower() and 'preview' not in name.lower():
                                        model_name = name
                                        break
                            
                            if not model_name:
                                print("No suitable Gemini model found")
                                job['gemini_analysis'] = "⚠️ **Gemini AI Analysis Unavailable**\n\nNo suitable Gemini AI models are available. This could be due to API quota limits or service disruption. Please try again later."
                                matched_jobs.append(job)
                                continue
                            
                            print(f"Using Gemini model: {model_name}")
                            model = genai.GenerativeModel(model_name)
                            
                            # Create prompt for job analysis with enhanced prompt for better job matching
                            if cv_text:
                                prompt = f"""
                                You are a professional job application advisor using the advanced Gemini 1.5 Flash model. Please analyze the following job description 
                                and the candidate's resume to provide a comprehensive assessment of the match:
                                
                                1. Job-Candidate Match Summary:
                                   - Provide a concise executive summary of the overall match (2-3 sentences)
                                   - Highlight the most significant matching points and gaps
                                   - Include a numerical match rating on a scale of 1-10 with decimal precision
                                
                                2. Key Requirements Analysis:
                                   - List the top 5-7 critical requirements from the job description
                                   - For each requirement, rate how well the candidate meets it (Excellent/Good/Partial/Missing)
                                   - Provide specific evidence from the resume for each rating
                                
                                3. Candidate Strengths for This Position:
                                   - Identify 3-5 specific strengths that make the candidate competitive
                                   - Explain how each strength directly addresses job requirements
                                
                                4. Critical Gaps and Mitigation Strategies:
                                   - Identify the most significant qualification gaps
                                   - For each gap, suggest how the candidate could address it in their application
                                   - Indicate which gaps might be dealbreakers vs. which can be overcome
                                
                                5. Application Strategy:
                                   - Provide 3-5 specific talking points for the candidate to emphasize
                                   - Suggest how to frame existing experience to better align with this specific job
                                
                                Job Description:
                                {job_desc}
                                
                                Candidate's Resume:
                                {cv_text}
                                
                                Provide your analysis in a structured format with clear headings. Be specific, actionable, and honest in your assessment.
                                """
                            else:
                                prompt = f"Analyze this job description and provide key insights: {job_desc}"
                            
                            # Generate the analysis
                            response = model.generate_content(prompt)
                            job['gemini_analysis'] = response.text
                        else:
                            job['gemini_analysis'] = "⚠️ **Gemini AI Analysis Unavailable**\n\nThe Google Gemini API service is currently unavailable. Basic matching is still working using semantic similarity."

                    except Exception as gemini_error:
                        print(f"Error getting Gemini analysis: {str(gemini_error)}")
                        job['gemini_analysis'] = "⚠️ **Gemini AI Analysis Error**\n\nAn error occurred while analyzing this job with Gemini AI. Basic matching is still working using semantic similarity."
                    
                    matched_jobs.append(job)
                    print(f"Matched job: {job['title']} with score {score:.2f}")
                else:
                    print(f"No description found for job: {job['title']}")
            except Exception as e:
                print(f"Error matching job {job.get('title', 'unknown')}: {str(e)}")
                print(traceback.format_exc())
        
        # Sort by match score in descending order
        sorted_jobs = sorted(matched_jobs, key=lambda x: x['match_score'], reverse=True)
        return sorted_jobs
    except Exception as e:
        print(f"Error in job matching: {str(e)}")
        print(traceback.format_exc())
        return []