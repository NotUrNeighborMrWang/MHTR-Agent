import requests
import openai
import base64
import os
import time


current_date = time.strftime("%Y-%m-%d", time.localtime())
base_url = 'https://api.openai.com/v1/chat/completions'



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def use_gpt_4v(image_path,api_key):
    
    base64_image = encode_image(image_path)
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2024-10
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
    Read the uploaded image, which is sourced from academic literature regarding carburizing heat treatment. The image may contain text, diagrams, figures, and tables relevant to carburizing processes, techniques, and effects on material properties. Your task is to determine if a table is present in the image. If a table is detected, respond with 'Yes' and transcribe the entire table, including its title, headers, body, and any footer or notes, in Markdown format. If no table is present, respond with 'No'.

Response format:
{Yes or No}
{Table if applicable}
"""
            },
            {
                "type": "image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail":"high"
                }
            }
            ]
        }
        ]}
    try:
        response = requests.post(base_url, headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        print(response.text)
        print('sleep 60s.....')
        time.sleep(60)
        response = requests.post(base_url, headers=headers, json=payload)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers


def use_gpt_4(api_key,input_information):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
   
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2024-10
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
# Task Description
You are an AI assistant with expertise in carburizing heat treatment. After reading and understanding the entire article, please complete the following tasks:
1. Extract the basic information of the article (such as title, authors, institutions, publication year, etc.) and save it in the Basic information section of the json file.
2. Summarize the main content of the research, research question, experimental design, experimental results, and other relevant parts of the article, and save them in the Content summary section of the json file.
3.Extract key information on carburizing heat treatment from the article, and save it in the json file to reflect the relationship between “materials - process parameters - microstructure - final properties” during carburizing.

# json Requirements
- **Basic information**
- **Content summary**
- **Column Headings:**
    a. Name of material (type of material)
    b. Carbon Flux (g/cm²·s)
    c. Diffusion Coefficient
    d. Saturated Carbon Concentration (wt%)
    e. Temperature (°C)
    f. Initial and Final Carbon Concentration
    g. Carburized Layer Depth (mm)
    h. Pulse and Diffusion Time (s)
    i. Gas Flow Rate (L/min or L/s)
    j. Carburizing Pressure (Pa)
    k. Other important parameters and details


# Data Organization Guidelines
- For non-numeric values, use strings whenever possible to prevent JSON file format errors.
- Content summary section Please consider a summary of the core content of this study for me to call upon when batch analyzing trends in the paper.
- Please analyze the materials used in the paper and analyze the categories of materials described
- Record the method used to measure carbon flux (e.g., segmented averaging or overall averaging) if specified in the document.
- Record specific diffusion models or calculation methods, particularly those adjusted for alloy compositions.
- If critical concentrations to avoid carbide networks are mentioned, record these values to prevent network carbide formation.
- Document the quenching oil temperature and cooling control methods to understand how heat treatment affects microstructure.
- If gradients from surface to core are detailed, record these values to analyze carburized depth and diffusion uniformity.
- Document hardness changes within the carburized layer if hardness values are given at different depths to validate the effective layer depth.
- If there are multiple diffusion stages, record each stage's timing arrangement.
- Include acetylene or nitrogen gas flow rates (L/min) and any noted effects on carbon concentration.
- Document the vacuum pressure in Pa, especially noting any differences in pressure for different gases or stages.
- Others guideline (If you can find or understand the relevant content from the paper, these contents are mostly in the table):
    - 1. Grain Boundary and Microstructural Characteristics: Note carbide morphology, size, and distribution within the microstructure, as observed under SEM, TEM, or other microscopy methods.
    - 2. Carbide Elemental Analysis: If EDS analysis is performed, document the main elemental composition of carbides (e.g., Cr, Nb, Mo) to understand their influence on carbon diffusion.
    - 3. Microhardness after Heat Treatment: Record surface hardness, maximum hardness, and hardness gradient distributions to assess process strengthening effects.
    - 4. Models and Calculation Methods: Record any carburizing models or equations used (such as modified Fick’s law) and calibration methods.

# Response format
Save the extracted information directly in JSON format without any surrounding markers or code block indicators.
==============================================================

""" + input_information
            }
            ]
        }
        ]}
    try:
        response = requests.post(base_url, headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        raise Exception(response.text)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers
