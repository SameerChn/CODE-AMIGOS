import sys
import importlib.util

def test_gemini_config():
    """Test if the Gemini API is properly configured in utils.py."""
    print("\n===== Testing Gemini Configuration in utils.py =====\n")
    
    # Check if utils module can be imported
    try:
        print("Importing utils module...")
        spec = importlib.util.spec_from_file_location("utils", "utils.py")
        utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils)
        print("✅ utils module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import utils module: {str(e)}")
        return False
    
    # Check if GEMINI_AVAILABLE is True
    try:
        print("\nChecking GEMINI_AVAILABLE flag...")
        if hasattr(utils, 'GEMINI_AVAILABLE'):
            if utils.GEMINI_AVAILABLE:
                print(f"✅ GEMINI_AVAILABLE is True - Gemini API is configured")
            else:
                print(f"❌ GEMINI_AVAILABLE is False - Gemini API is not configured")
                print(f"Reason: {utils.GEMINI_ERROR if hasattr(utils, 'GEMINI_ERROR') else 'Unknown'}")
                return False
        else:
            print("❌ GEMINI_AVAILABLE flag not found in utils module")
            return False
    except Exception as e:
        print(f"❌ Error checking GEMINI_AVAILABLE: {str(e)}")
        return False
    
    # Check if genai is imported and configured
    try:
        print("\nChecking if genai is imported and configured...")
        if hasattr(utils, 'genai'):
            print("✅ genai is imported in utils module")
            
            # Try to list models to verify configuration
            try:
                print("\nTrying to list models to verify configuration...")
                models = utils.genai.list_models()
                model_names = [model.name for model in models]
                print(f"✅ Successfully listed {len(model_names)} models")
                
                # Find gemini models
                gemini_models = [name for name in model_names if 'gemini' in name.lower()]
                if gemini_models:
                    print(f"Found {len(gemini_models)} Gemini models")
                    print("First 3 models:")
                    for i, model in enumerate(gemini_models[:3], 1):
                        print(f"{i}. {model}")
                else:
                    print("⚠️ No Gemini models found in available models")
            except Exception as e:
                print(f"❌ Failed to list models: {str(e)}")
                if "quota" in str(e).lower() or "429" in str(e):
                    print("\n⚠️ API QUOTA EXCEEDED - This is likely the cause of your issues")
                return False
        else:
            print("❌ genai is not imported in utils module")
            return False
    except Exception as e:
        print(f"❌ Error checking genai configuration: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_gemini_config()
    
    print("\n===== Summary =====")
    if success:
        print("✅ Gemini API is properly configured in utils.py!")
        print("The application should be able to use Gemini AI features.")
    else:
        print("❌ Gemini API configuration check failed.")
        print("The application may not be able to use Gemini AI features.")
        print("Check the specific error messages above for more details.")