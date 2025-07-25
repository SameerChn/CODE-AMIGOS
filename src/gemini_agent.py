import google.generativeai as genai
 
# ✅ Your Gemini API key 
API_KEY = "AIzaSyAa97pSL3kb1yEvoaj6vpi8LCeN6aRvMPk" 
 
# 🔧 Configure the Gemini API 
genai.configure(api_key=API_KEY) 
 
# 🧠 Load the Gemini 1.5 Flash Latest model 
model = genai.GenerativeModel("models/gemini-1.5-flash-latest") 
 
def main(): 
    print("💬 Gemini AI Agent (type 'exit' to quit)") 
    while True: 
        user_input = input("You: ") 
 
        if user_input.lower() in ['exit', 'quit']: 
            print("👋 Exiting Gemini AI Agent. Goodbye!") 
            break 
 
        try: 
            response = model.generate_content(user_input) 
            print("Gemini:", response.text.strip()) 
        except Exception as e: 
            print("⚠️ Error:", e) 
 
if __name__ == "__main__": 
    main()