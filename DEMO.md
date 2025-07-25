# CVision: Smart Job Finder - Demo

## Video Demo Link

[Watch the full demo video here](https://youtu.be/your-video-id)

## Video Timestamps

### Introduction and Overview
- **00:00 - 00:30** - Introduction to CVision: Smart Job Finder
- **00:30 - 01:00** - Overview of key features and capabilities

### Resume Upload and Analysis
- **01:00 - 01:30** - Uploading a resume (PDF/DOCX)
- **01:30 - 02:00** - Automatic domain detection
- **02:00 - 02:30** - Skills extraction and categorization
- **02:30 - 03:30** - Gemini AI resume analysis

### Job Search and Matching
- **03:30 - 04:00** - Selecting job platforms
- **04:00 - 04:30** - Initiating job search
- **04:30 - 05:30** - Viewing matched jobs and similarity scores
- **05:30 - 06:30** - Gemini AI job description analysis

### Manual Text Analysis
- **06:30 - 07:00** - Using the manual text analysis feature
- **07:00 - 08:00** - Reviewing Gemini AI text analysis results

### Advanced Features
- **08:00 - 09:00** - Customizing job search parameters
- **09:00 - 10:00** - Comparing multiple job opportunities
- **10:00 - 11:00** - Using the application without a resume (manual domain entry)

### Conclusion
- **11:00 - 12:00** - Summary of benefits and use cases
- **12:00 - 12:30** - Future enhancements and roadmap

## Installation Instructions

To run this demo on your local machine:

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Tesseract OCR (if needed for image-based PDFs)
4. Set up your Google Gemini API key
5. Run the application:
   ```
   streamlit run main.py
   ```

## Setting Up the Gemini API Key

To use the Gemini AI features, you need to provide your Gemini API key in a `.env` file:

1. In the `src` directory (or project root), create a file named `.env` if it does not already exist.
2. Open the `.env` file and add the following line, replacing `your-gemini-api-key-here` with your actual API key:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
3. Save the file. The application will automatically load this key when you run it.

## System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for job scraping and Gemini AI integration
- Tesseract OCR (optional, for image-based PDFs)
- Google Gemini API key (for AI analysis features)

## Notes

- The demo showcases the application with a technical resume in the software development domain
- Job search results may vary based on current job market conditions
- Gemini AI analysis requires a valid API key and quota availability