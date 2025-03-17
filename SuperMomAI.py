# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mNLCgAGwESZ6nYYReqBOZ3y_9K1Eck_y
"""

!pip install python-dotenv

!ls /content

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv("/content/.env")

# Retrieve API Key
HF_API_KEY = os.getenv("HF_API_KEY")

# Check if the key is loaded
print("API Key loaded successfully!" if HF_API_KEY else "API Key not found!")

!pip install gradio python-dotenv requests

!pip install --upgrade --force-reinstall gradio python-dotenv requests torch torchvision torchaudio

import os
import gradio as gr
import requests
from dotenv import load_dotenv

# ✅ Load the .env file
load_dotenv("/content/.env")  # Ensure this path is correct

# ✅ Fetch API Key securely
HF_API_KEY = os.getenv("HF_API_KEY")

# ✅ Check if API Key is loaded
if not HF_API_KEY:
    raise ValueError("❌ API Key not found! Make sure .env file is properly loaded.")

# 🔹 Choose a Reliable Model
model_name = "HuggingFaceH4/zephyr-7b-beta"  # ⬅️ Try this if the previous one fails

# 🔹 Define System Message
system_message = """You are SuperMom Guide, an AI parenting assistant.
Your goal is to provide clear, practical, and step-by-step parenting advice.
You will give only **real-world parenting solutions** with no fiction.
"""

# 🔹 Function to Call Hugging Face API with Fixes
def ask_supermom(question):
    """Securely send a request to the Hugging Face API and get a structured response."""
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "inputs": f"<s>[INST] {system_message}\n\nUser: {question} [/INST]>",
        "parameters": {"max_new_tokens": 200, "temperature": 0.7, "top_p": 0.9},
    }

    try:
        response = requests.post(f"https://api-inference.huggingface.co/models/{model_name}", headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()

            # ✅ Ensure response is properly structured
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"].strip()
            else:
                return "⚠️ Unexpected response format. Try another model."

        else:
            return f"❌ API Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"❌ Network Error: {str(e)}"

# 🔹 Gradio Interface for Public Sharing
interface = gr.Interface(
    fn=ask_supermom,
    inputs=gr.Textbox(lines=2, placeholder="Ask SuperMom Bot anything..."),
    outputs=gr.Textbox(),
    title="SuperMom Bot",
    description="Get practical, real-world parenting advice from SuperMom Bot!",
)

# 🔹 Launch Gradio App with Public Sharing
interface.launch(share=True)

