import google.generativeai as genai
import os
import sys
import time

def test_gemini_models(api_key=None):
    """Test different Gemini models to find which ones are available and working."""
    print("\n===== Google Gemini Models Test =====\n")
    
    # Use provided API key or try to get from environment
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY", None)
        if not api_key:
            print("⚠️ No API key provided and GOOGLE_API_KEY environment variable not found.")
            print("Please provide an API key as an argument: python test_gemini_models.py YOUR_API_KEY")
            return
    
    # Configure the API
    try:
        print(f"Configuring Gemini API with provided key...")
        genai.configure(api_key=api_key)
        print("✅ API configuration successful")
    except Exception as e:
        print(f"❌ API configuration failed: {str(e)}")
        return
    
    # List available models
    try:
        print("\nListing available models...")
        models = genai.list_models()
        model_names = [model.name for model in models]
        
        # Filter for Gemini models
        gemini_models = [name for name in model_names if 'gemini' in name.lower()]
        
        if not gemini_models:
            print("No Gemini models found in your available models.")
            return
            
        print(f"Found {len(gemini_models)} Gemini models.")
        
        # Test each model
        working_models = []
        quota_exceeded_models = []
        other_error_models = []
        
        for i, model_name in enumerate(gemini_models, 1):
            print(f"\n[{i}/{len(gemini_models)}] Testing model: {model_name}")
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, please respond with a single word: Working")
                print(f"✅ SUCCESS! Response: {response.text}")
                working_models.append((model_name, response.text))
            except Exception as e:
                error_msg = str(e)
                print(f"❌ ERROR: {error_msg}")
                
                if "quota" in error_msg.lower() or "429" in error_msg:
                    quota_exceeded_models.append((model_name, error_msg))
                else:
                    other_error_models.append((model_name, error_msg))
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        # Print summary
        print("\n===== Test Results =====\n")
        
        print(f"Total models tested: {len(gemini_models)}")
        print(f"Working models: {len(working_models)}")
        print(f"Quota exceeded models: {len(quota_exceeded_models)}")
        print(f"Other errors: {len(other_error_models)}")
        
        if working_models:
            print("\n✅ WORKING MODELS:")
            for i, (model, response) in enumerate(working_models, 1):
                print(f"{i}. {model} - Response: {response}")
        
        if quota_exceeded_models:
            print("\n⚠️ QUOTA EXCEEDED MODELS:")
            for i, (model, error) in enumerate(quota_exceeded_models, 1):
                print(f"{i}. {model}")
        
        if other_error_models:
            print("\n❌ MODELS WITH OTHER ERRORS:")
            for i, (model, error) in enumerate(other_error_models, 1):
                print(f"{i}. {model} - Error: {error}")
        
        # Recommend models to use
        if working_models:
            print("\n===== Recommended Models =====\n")
            print("Based on the test results, you can use these models in your application:")
            for i, (model, _) in enumerate(working_models, 1):
                print(f"{i}. {model}")
            
            print("\nTo use these models, update the 'preferred_models' list in utils.py")
        else:
            print("\n⚠️ No working models found. You may need to:")
            print("1. Check if you've exceeded your API quota")
            print("2. Verify your API key has access to Gemini models")
            print("3. Try again later as the service might be temporarily unavailable")
            
    except Exception as e:
        print(f"❌ Failed to list or test models: {str(e)}")

if __name__ == "__main__":
    # Get API key from command line argument if provided
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    test_gemini_models(api_key)