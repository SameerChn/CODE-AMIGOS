import google.generativeai as genai
import os
import sys

def check_gemini_status(api_key=None):
    """Check the status of Google Gemini API and available models."""
    print("\n===== Google Gemini API Status Check =====\n")
    
    # Use provided API key or try to get from environment
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY", None)
        if not api_key:
            print("⚠️ No API key provided and GOOGLE_API_KEY environment variable not found.")
            print("Please provide an API key as an argument: python check_gemini_status.py YOUR_API_KEY")
            return False
    
    # Configure the API
    try:
        print(f"Configuring Gemini API with provided key...")
        genai.configure(api_key=api_key)
        print("✅ API configuration successful")
    except Exception as e:
        print(f"❌ API configuration failed: {str(e)}")
        return False
    
    # List available models
    try:
        print("\nListing available models...")
        models = genai.list_models()
        model_names = [model.name for model in models]
        
        print(f"✅ Successfully retrieved {len(model_names)} models")
        
        # Find gemini models
        gemini_models = [name for name in model_names if 'gemini' in name.lower()]
        
        if gemini_models:
            print(f"\nFound {len(gemini_models)} Gemini models:")
            for i, model in enumerate(gemini_models, 1):
                print(f"{i}. {model}")
        else:
            print("\n⚠️ No Gemini models found in your available models.")
        
        # Check for specific models
        preferred_models = [
            'models/gemini-1.0-pro',
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro-latest',
            'models/gemini-1.5-flash',
            'models/gemini-flash',
            'models/gemini-pro'
        ]
        
        print("\nChecking for commonly used models:")
        available_preferred = []
        for model in preferred_models:
            if model in model_names:
                print(f"✅ {model} - AVAILABLE")
                available_preferred.append(model)
            else:
                print(f"❌ {model} - NOT AVAILABLE")
        
        # Test a model if available
        if available_preferred:
            test_model = available_preferred[0]
            print(f"\nTesting model {test_model}...")
            try:
                model = genai.GenerativeModel(test_model)
                response = model.generate_content("Hello, please respond with a single word: Working")
                print(f"✅ Test successful! Response: {response.text}")
                return True
            except Exception as e:
                print(f"❌ Test failed: {str(e)}")
                if "quota" in str(e).lower() or "429" in str(e):
                    print("\n⚠️ API QUOTA EXCEEDED - This is likely the cause of your issues.")
                    print("Google Gemini API has usage limits. You may need to wait or upgrade your quota.")
                return False
        else:
            print("\n⚠️ No preferred models available to test.")
            return False
            
    except Exception as e:
        print(f"❌ Failed to list models: {str(e)}")
        return False

if __name__ == "__main__":
    # Get API key from command line argument if provided
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    success = check_gemini_status(api_key)
    
    print("\n===== Summary =====")
    if success:
        print("✅ Gemini API is working correctly!")
        print("If you're still experiencing issues in your application, check your implementation.")
    else:
        print("❌ Gemini API check failed.")
        print("Possible solutions:")
        print("1. Check if your API key is correct")
        print("2. Verify your internet connection")
        print("3. Check if you've exceeded your API quota")
        print("4. Try again later as the service might be temporarily unavailable")