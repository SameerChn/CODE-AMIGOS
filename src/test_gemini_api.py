import google.generativeai as genai
import sys

def test_gemini_api():
    """Test if the Gemini API is working with the current API key."""
    print("\n===== Testing Gemini API =====\n")
    
    # Configure the API with the key from utils.py
    api_key = 'AIzaSyAa97pSL3kb1yEvoaj6vpi8LCeN6aRvMPk'
    try:
        print(f"Configuring Gemini API...")
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
            print(f"\nFound {len(gemini_models)} Gemini models")
            print("First 5 models:")
            for i, model in enumerate(gemini_models[:5], 1):
                print(f"{i}. {model}")
        else:
            print("\n⚠️ No Gemini models found in your available models.")
            return False
        
        # Find a working model
        print("\nFinding a working model...")
        working_models = []
        
        # Try flash models first (more likely to be in free tier)
        flash_models = [name for name in gemini_models if 'flash' in name.lower()]
        if flash_models:
            test_model = flash_models[0]
            print(f"Testing flash model: {test_model}")
            try:
                model = genai.GenerativeModel(test_model)
                response = model.generate_content("Hello, respond with a single word: Test")
                print(f"✅ Test successful! Response: {response.text}")
                working_models.append(test_model)
            except Exception as e:
                print(f"❌ Test failed: {str(e)}")
                if "quota" in str(e).lower() or "429" in str(e):
                    print("\n⚠️ API QUOTA EXCEEDED - This is likely the cause of your issues.")
        
        # If no flash models worked, try any other model
        if not working_models and len(gemini_models) > 0:
            test_model = gemini_models[0]
            print(f"Testing alternative model: {test_model}")
            try:
                model = genai.GenerativeModel(test_model)
                response = model.generate_content("Hello, respond with a single word: Test")
                print(f"✅ Test successful! Response: {response.text}")
                working_models.append(test_model)
            except Exception as e:
                print(f"❌ Test failed: {str(e)}")
                if "quota" in str(e).lower() or "429" in str(e):
                    print("\n⚠️ API QUOTA EXCEEDED - This is likely the cause of your issues.")
        
        # Summary
        if working_models:
            print("\n✅ Gemini API is working with at least one model!")
            print(f"Working models: {', '.join(working_models)}")
            return True
        else:
            print("\n❌ No working Gemini models found.")
            print("This could be due to API quota limits or service disruption.")
            return False
            
    except Exception as e:
        print(f"❌ Failed to list or test models: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    
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