# CVision: Smart Job Finder - System Architecture

## System Overview

CVision is an AI-powered job matching system that analyzes resumes and job descriptions to help users find the most suitable job opportunities. The system leverages advanced NLP techniques and Google's Gemini AI to provide intelligent matching and detailed analysis.

## Architecture Diagram

```
+---------------------+     +----------------------+     +---------------------+
|                     |     |                      |     |                     |
|  User Interface     |     |  Core Processing     |     |  External Services  |
|  (Streamlit)        |     |  Engine              |     |  & APIs             |
|                     |     |                      |     |                     |
+----------+----------+     +-----------+----------+     +---------+-----------+
           |                            |                          |
           v                            v                          v
+----------+----------------------------+-----+     +-------------+------------+
|                                            |     |                          |
|  Document Processing                       |     |  Job Scraping Services   |
|  - PDF/DOCX Extraction                     |     |  - LinkedIn              |
|  - OCR (Tesseract)                         |     |  - Upwork                |
|  - Text Cleaning                           |     |  - Fiverr                |
|                                            |     |  - Indeed                |
+--------------------+---------------------+      |  - Naukri.com            |
                     |                            |  - Internshala           |
                     v                            |                          |
+--------------------+---------------------+     +-------------+------------+
|                                          |                  |
|  AI Analysis Components                  |                  |
|  - Domain Classification                 |                  |
|  - Skills Extraction                     |                  |
|  - Resume Analysis (Gemini)              |<-----------------+
|  - Job Description Analysis (Gemini)     |
|  - Job-Resume Matching                   |
|                                          |
+------------------------------------------+
```

## Component Breakdown

### 1. Planner

The planner component orchestrates the overall workflow of the application:

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
| Input Collection |---->| Analysis Planning|---->| Results Assembly |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

- **Input Collection**: Gathers user inputs (resume upload or manual domain entry)
- **Analysis Planning**: Determines which analyses to run based on available inputs
- **Results Assembly**: Organizes analysis results for presentation to the user

### 2. Executor

The executor component handles the actual processing tasks:

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
| Text Extraction  |---->| Feature Analysis |---->| Job Matching     |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

- **Text Extraction**: Extracts text from uploaded documents (PDF/DOCX)
- **Feature Analysis**: Analyzes extracted text for domain, skills, etc.
- **Job Matching**: Matches resume with job listings using semantic similarity

### 3. Memory Structure

The application uses Streamlit's session state as its memory structure:

```
+------------------------------------------+
|                                          |
|  Session State Memory                    |
|  +----------------------------------+    |
|  |  cv_text: Extracted resume text  |    |
|  +----------------------------------+    |
|  +----------------------------------+    |
|  |  domain: Detected job domain     |    |
|  +----------------------------------+    |
|  +----------------------------------+    |
|  |  skills: Extracted skills list   |    |
|  +----------------------------------+    |
|  +----------------------------------+    |
|  |  jobs: Matched job listings      |    |
|  +----------------------------------+    |
|  +----------------------------------+    |
|  |  gemini_analysis: AI analysis    |    |
|  +----------------------------------+    |
|  +----------------------------------+    |
|  |  gemini_api_key: API credentials |    |
|  +----------------------------------+    |
|                                          |
+------------------------------------------+
```

### 4. Tool Integration

#### Gemini AI Integration

```
+------------------------------------------+
|                                          |
|  Gemini AI Integration                   |
|  +----------------------------------+    |
|  |  Model Selection Logic           |    |
|  |  - Prioritize gemini-1.5-flash-  |    |
|  |    latest                        |    |
|  |  - Fallback to gemini-1.5-flash  |    |
|  |  - Try other available models    |    |
|  +----------------------------------+    |
|                                          |
|  +----------------------------------+    |
|  |  Analysis Functions              |    |
|  |  - analyze_resume_with_gemini    |    |
|  |  - analyze_job_description_with_ |    |
|  |    gemini                        |    |
|  |  - analyze_manual_text_with_     |    |
|  |    gemini                        |    |
|  |  - match_jobs (with Gemini       |    |
|  |    enhancement)                  |    |
|  +----------------------------------+    |
|                                          |
+------------------------------------------+
```

#### Other Tools

- **Tesseract OCR**: For extracting text from image-based PDFs
- **SentenceTransformer**: For semantic similarity matching between resumes and jobs
- **spaCy**: For NLP tasks like entity recognition and text processing
- **Web Scraping Tools**: For retrieving job listings from various platforms

### 5. Observability

```
+------------------------------------------+
|                                          |
|  Observability Components                |
|  +----------------------------------+    |
|  |  Console Logging                 |    |
|  |  - Detailed process logging      |    |
|  |  - Error tracking with           |    |
|  |    tracebacks                    |    |
|  +----------------------------------+    |
|                                          |
|  +----------------------------------+    |
|  |  User Feedback                   |    |
|  |  - Success/error messages        |    |
|  |  - Process indicators            |    |
|  |  - Analysis results display      |    |
|  +----------------------------------+    |
|                                          |
|  +----------------------------------+    |
|  |  Diagnostic Tools                |    |
|  |  - Tesseract availability check  |    |
|  |  - Gemini API status check      |    |
|  |  - Model availability testing    |    |
|  +----------------------------------+    |
|                                          |
+------------------------------------------+
```

## Data Flow

1. User uploads resume or enters job domain
2. System extracts text from resume (if uploaded)
3. System analyzes resume to determine domain and extract skills
4. System scrapes job listings from selected platforms
5. System matches resume with job listings using semantic similarity
6. System enhances matches with Gemini AI analysis
7. System presents results to user with detailed insights

## Integration Points

- **Google Gemini AI**: For advanced resume and job description analysis
- **Job Platforms**: LinkedIn, Upwork, Fiverr, Indeed, Naukri.com, Internshala
- **Document Processing**: PDF, DOCX, and image-based document handling
- **User Interface**: Streamlit-based web interface

## Scalability Considerations

- The current architecture is designed for individual use
- For scaling to multiple users, consider:
  - Moving to a client-server architecture
  - Implementing job data caching
  - Adding a database for persistent storage
  - Implementing rate limiting for API calls
  - Adding authentication and user profiles