import google.generativeai as genai

# Configure the API
genai.configure(api_key='AIzaSyAa97pSL3kb1yEvoaj6vpi8LCeN6aRvMPk')

# List available models
print('Available models:')
available_models = []
try:
    for model in genai.list_models():
        print(f"- {model.name}")
        available_models.append(model.name)
except Exception as e:
    print(f"Error listing models: {e}")

# Try to generate content with an available model
print('\nTrying to generate content:')
try:
    # Try with models that might be in the free tier
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
    
    model_to_try = None
    
    # First try preferred models
    for preferred in preferred_models:
        if preferred in available_models:
            model_to_try = preferred
            break
    
    # If no preferred models found, try any model with 'flash' in the name (likely to be in free tier)
    if not model_to_try:
        for model_name in available_models:
            if 'flash' in model_name.lower() and 'preview' not in model_name.lower():
                model_to_try = model_name
                break
    
    if model_to_try:
        print(f"Using model: {model_to_try}")
        model = genai.GenerativeModel(model_to_try)
        response = model.generate_content('Say hello world')
        print(f"Response: {response.text}")
    else:
        print("No suitable models found")
except Exception as e:
    print(f"Error generating content: {e}")