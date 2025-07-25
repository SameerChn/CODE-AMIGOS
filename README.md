# CVision: Smart Job Finder

CVision is an AI-powered application that analyzes your resume/CV and helps you find matching jobs based on your skills and experience. It uses natural language processing, OCR technology, and Google's Gemini AI to provide intelligent job matching and analysis.

## Features

- **Resume Analysis**: Extract skills, experience, and domain from your CV
- **OCR Support**: Process image-based PDFs using Tesseract OCR
- **AI-Powered Analysis**: Get detailed insights about your CV using Google Gemini AI
- **Job Matching**: Find jobs that match your skills across multiple platforms
- **Job Analysis**: Analyze job descriptions and get personalized recommendations

## Requirements

- Python 3.8+
- Tesseract OCR (for processing image-based PDFs)
- Google Gemini API key (for AI analysis features)

## Installation

1. Clone this repository or download the source code

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:

   - **Windows**: Run the included installer script:
     ```bash
     python install_tesseract.py
     ```
     Or download and install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   
   - **macOS**: Install using Homebrew:
     ```bash
     brew install tesseract
     ```
   
   - **Linux**: Install using your package manager:
     ```bash
     sudo apt-get install tesseract-ocr
     ```

## Setting Up the Gemini API Key

To use the Gemini AI features, you need to provide your Gemini API key in a `.env` file:

1. In the `src` directory (or project root), create a file named `.env` if it does not already exist.
2. Open the `.env` file and add the following line, replacing `your-gemini-api-key-here` with your actual API key:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
3. Save the file. The application will automatically load this key when you run it.

## Running the Application

```bash
streamlit run main.py
```

The application will open in your default web browser.

## Using the Application

1. **Upload your CV**: Use the sidebar to upload your resume in PDF or DOCX format

2. **Enable AI Analysis**: Toggle the Gemini AI Analysis option to get advanced insights

3. **View Analysis**: See extracted skills, domain, and AI-powered analysis of your CV

4. **Find Matching Jobs**: The application will search for jobs matching your profile

5. **Analyze Job Descriptions**: Get AI-powered analysis of job descriptions and how well they match your profile

## Troubleshooting

### Tesseract OCR Issues

If you encounter issues with OCR functionality:

1. Make sure Tesseract OCR is properly installed
2. The application will show a warning if Tesseract is not found
3. Use the "Install Tesseract OCR" button in the application to install it
4. After installation, restart the application

### Google Gemini API Issues

If you encounter issues with the Gemini AI features:

1. Check if your API key is valid
2. You may have exceeded your API quota (common with free tier)
3. Try again later or use a different API key
4. See the GEMINI_TROUBLESHOOTING.md file for more details

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors / Author

- [Aryan Kumar](https://github.com/aryacreations) - aryanrajput5760@gmail.com
- [Sumit Sinha](https://github.com/thesumitsinhaa) - sumitsinharcet@gmail.com
- [Sameer Kumar](https://github.com/SameerChn) - chauhan.sameer3101@gmail.com
- [vipul Kumar Sahil]() - vipulsahil76320@gmail.com