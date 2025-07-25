# CVision: Smart Job Finder - Demo

## Video Demo Link

[Youtube demo video](https://youtu.be/4T3NQJNMNlg)

## Video Timestamps

### Introduction and Overview
- **00:00 - 00:15** - Introduction to CVision: Smart Job Finder.
- **00:15 - 00:45** - Overview of key code.
- **01:00 - 01:30** - Manual input for job searching USING Google's Gemini AI to provide intelligent job matching and analysis.
- **01:30 - 04:45** - Resume/CV upload for job finding, Google's Gemini AI to provide intelligent job matching and analysis.

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