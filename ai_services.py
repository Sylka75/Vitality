import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

def analyze_meal(image):
    """Uses Gemini 1.5 Flash to analyze the image and return structured nutritional data."""
    try:
        gemini_key = st.secrets.get("GEMINI_API_KEY")
        if not gemini_key:
            return {"error": "GEMINI_API_KEY missing in secrets."}
        
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Resize image for faster processing (max 1024px)
        max_size = (1024, 1024)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        prompt = """
        You are an expert nutritionist. Analyze this food image and:
        1. Identify the main dish/items.
        2. Estimate the total calories for the portion shown.
        3. Pick one single emoji that best represents the meal.
        
        Respond ONLY in valid JSON format matching this schema:
        {
            "label": "Short name of the food (e.g., Avocado Toast)",
            "calories": 350,
            "emoji": "🥑"
        }
        """
        
        response = model.generate_content([prompt, image])
        # Try to find JSON in the response
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        
        result = json.loads(text)
        return result
    except Exception as e:
        return {"error": f"Gemini Analysis Error: {str(e)}"}

# Keeping old names for compatibility if needed, but pointing to the new better service
def describe_image(image):
    # This is now handled in one step by analyze_meal
    return "Analysis handled by Gemini"

def parse_food_description(description: str):
    # This is now handled in one step by analyze_meal
    return {}
