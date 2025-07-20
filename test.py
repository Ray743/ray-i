import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the .env file and set the API key
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Ask it something
response = model.generate_content("Explain how AI works in a few words")
print(response.text)
