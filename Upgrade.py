import streamlit as st
import requests
import time

st.title("Script to Image Prompt Generator")
st.write("This app generates image prompts for each line of your video script.")

# User input for script
script_text = st.text_area("Paste your script here:", height=300)
api_token = st.text_input("Hugging Face API Token", type="password")

# Updated to better model for creative generation
model_name = "EleutherAI/gpt-neo-2.7B"
API_URL = f"https://api-inference.huggingface.co/models/{model_name}"

def generate_image_prompt(script_line, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    
    # Improved prompt structure
    prompt_template = f"""Convert this script line to a detailed image prompt. 
    Include visual elements, colors, and mood.
    Script Line: {script_line}
    Image Prompt:"""
    
    payload = {
        "inputs": prompt_template,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.9,
            "return_full_text": False  # Get only the generated text
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Handle model loading wait time
        if response.status_code == 503:
            wait_time = response.json().get('estimated_time', 30)
            time.sleep(wait_time)
            response = requests.post(API_URL, headers=headers, json=payload)
            
        if response.status_code != 200:
            return f"API Error: {response.status_code}"
            
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', 'No prompt generated').strip()
        return "No response generated"
        
    except Exception as e:
        return f"Error: {str(e)}"

if st.button("Generate Image Prompts"):
    if not api_token:
        st.error("API Token is required!")
    elif not script_text:
        st.error("Please enter script text!")
    else:
        lines = [line.strip() for line in script_text.split("\n") if line.strip()]
        st.write(f"Processing {len(lines)} lines...")
        
        prompts = {}
        for idx, line in enumerate(lines, 1):
            with st.spinner(f"Generating prompt for line {idx}..."):
                prompt = generate_image_prompt(line, api_token)
                # Clean any extra text after prompt
                prompts[line] = prompt.split('\n')[0].strip()
                
        st.write("## Generated Prompts:")
        for script_line, prompt in prompts.items():
            st.markdown(f"**Script Line:** `{script_line}`")
            st.markdown(f"**Image Prompt:** {prompt}")
            st.markdown("---")
