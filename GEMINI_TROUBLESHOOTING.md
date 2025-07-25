# Google Gemini API Troubleshooting Guide

If you're experiencing issues with the Google Gemini API in this application, this guide will help you diagnose and resolve common problems.

## Common Issues

### 1. API Quota Exceeded

The most common issue with the Gemini API is exceeding your quota limits. Google provides limited free usage, and once exceeded, you'll need to wait for the quota to reset or upgrade to a paid tier.

**Symptoms:**
- Error messages containing "quota exceeded" or "429" status codes
- The application shows warnings about Gemini being unavailable
- Analysis features don't work despite having a valid API key

**Solutions:**
- Wait for your quota to reset (typically daily)
- Create a new Google Cloud project with a new API key
- Upgrade to a paid tier for higher quotas

### 2. API Key Issues

**Symptoms:**
- Authentication errors
- "API key not valid" messages

**Solutions:**
- Verify your API key is correct and properly formatted
- Generate a new API key in the Google Cloud Console
- Ensure the API key has access to the Gemini API

### 3. Model Availability

**Symptoms:**
- "Model not found" errors
- 404 errors when trying to use specific models

**Solutions:**
- Check which models are available to your account
- Some models may be in limited preview or not available in your region
- Try using a different model version

## Checking Your Gemini API Status

This application includes a diagnostic tool to check your Gemini API status:

```bash
python check_gemini_status.py YOUR_API_KEY
```

Replace `YOUR_API_KEY` with your Google Gemini API key. This script will:

1. Verify your API key configuration
2. List available models
3. Test a simple API call
4. Provide a summary of any issues found

## Updating Your API Key

To update your API key in the application:

1. Open `utils.py`
2. Find the line with `genai.configure(api_key="YOUR_API_KEY_HERE")`
3. Replace the existing key with your new API key
4. Save the file and restart the application

## Getting a New API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and update it in the application

## Alternative Models

The application has been updated to try multiple Gemini models if the primary one is unavailable. It will attempt to use:

1. gemini-1.0-pro
2. gemini-1.5-pro
3. gemini-1.0-pro-latest
4. gemini-1.5-flash
5. Various other flash models

If none of these models are available, the application will gracefully degrade and continue to function with basic features.

## Still Having Issues?

If you're still experiencing problems after trying these solutions:

1. Check the Google Gemini API status page for service disruptions
2. Verify your internet connection
3. Try running the application from a different network
4. Contact Google Cloud support if you have a paid account