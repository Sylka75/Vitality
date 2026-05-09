import streamlit as st
import requests
import base64
from io import BytesIO
from google import genai
from google.genai import types
import json

HF_API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"

def describe_image(image):
    try:
        hf_token = st.secrets.get("HF_TOKEN")
        if not hf_token:
            return "Error: HF_TOKEN missing in secrets."
        
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Convert PIL Image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Llava payload
        payload = {
            "inputs": f"data:image/jpeg;base64,{img_str}",
            "parameters": {
                "prompt": "USER: <image>\nDescribe this food in detail. What are the ingredients and portion sizes?\nASSISTANT:"
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        res_json = response.json()
        if isinstance(res_json, list) and len(res_json) > 0 and 'generated_text' in res_json[0]:
            text = res_json[0]['generated_text']
            if "ASSISTANT:" in text:
                return text.split("ASSISTANT:")[1].strip()
            return text
        return str(res_json)
    except Exception as e:
        return f"Error with Vision API: {e}"

def parse_food_description(description: str):
    try:
        gemini_key = st.secrets.get("GEMINI_API_KEY")
        if not gemini_key:
            return {"error": "GEMINI_API_KEY missing in secrets."}
            
        client = genai.Client(api_key=gemini_key)
        
        prompt = f"""
        You are an expert nutritionist. I will provide a description of food from an image.
        Your task is to estimate the calories and provide a short label and an emoji.
        
        Description: {description}
        
        Respond ONLY in valid JSON format matching this schema:
        {{
            "label": "Short name of the food (e.g., Avocado Toast)",
            "calories": 350,
            "emoji": "🥑"
        }}
        """
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {"error": str(e)}
